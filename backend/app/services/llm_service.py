import httpx
import json
import hashlib
import time
import re
from typing import Optional, Dict, Any, List, Tuple

from app.core.config import settings


class LLMParseCache:
    """内存缓存，用于存储 LLM 解析结果"""
    def __init__(self, ttl_seconds: int = 30 * 24 * 3600):  # 默认 30 天
        self._cache: Dict[str, Tuple[float, Dict[str, Any]]] = {}
        self._ttl = ttl_seconds

    def get(self, key: str) -> Optional[Dict[str, Any]]:
        if key in self._cache:
            timestamp, value = self._cache[key]
            if time.time() - timestamp < self._ttl:
                return value
            else:
                del self._cache[key]
        return None

    def set(self, key: str, value: Dict[str, Any]) -> None:
        self._cache[key] = (time.time(), value)

    def clear(self) -> None:
        self._cache.clear()


def is_chinese_text(text: str) -> bool:
    """检测文本是否主要为中文"""
    if not text:
        return True  # 空文本视为无需翻译
    
    # 统计中文字符比例
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
    total_chars = len(re.sub(r'\s', '', text))  # 排除空白字符
    
    if total_chars == 0:
        return True
    
    # 如果中文字符占比超过 30%，认为是中文文本
    return chinese_chars / total_chars > 0.3


class LLMService:
    def __init__(self):
        self.api_key = settings.LLM_API_KEY
        self.api_url = settings.LLM_API_URL
        self.model = settings.LLM_MODEL
        self.cache = LLMParseCache(ttl_seconds=settings.CACHE_TTL_LLM_PARSE)
        self._translation_cache: Dict[str, str] = {}  # 翻译缓存

    def _generate_cache_key(self, name: str, description: str) -> str:
        """生成基于名称和描述的缓存键"""
        content = f"{name}:{description}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def _generate_translation_cache_key(self, text: str) -> str:
        """生成翻译缓存键"""
        return hashlib.md5(text.encode()).hexdigest()

    async def translate_to_chinese(
        self,
        text: str,
        use_cache: bool = True,
    ) -> str:
        """
        将文本翻译为中文
        - 如果文本已经是中文，直接返回原文
        - 如果没有 API Key，返回原文
        - 翻译失败时返回原文
        """
        if not text or not text.strip():
            return text
        
        # 检查是否已经是中文
        if is_chinese_text(text):
            return text
        
        # 检查翻译缓存
        cache_key = self._generate_translation_cache_key(text)
        if use_cache and cache_key in self._translation_cache:
            return self._translation_cache[cache_key]
        
        # 检查 API Key
        if not self.api_key:
            return text
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.api_url}/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": self.model,
                        "messages": [
                            {
                                "role": "system",
                                "content": "你是一个专业的翻译助手。请将用户提供的文本翻译成中文。只返回翻译结果，不要添加任何解释或额外内容。"
                            },
                            {
                                "role": "user",
                                "content": f"请将以下文本翻译成中文：\n\n{text}"
                            },
                        ],
                        "temperature": 0.3,
                    },
                    timeout=60.0,
                )
                response.raise_for_status()
                result = response.json()
                
                translated = result["choices"][0]["message"]["content"].strip()
                
                # 缓存翻译结果
                if use_cache:
                    self._translation_cache[cache_key] = translated
                
                return translated
                
        except Exception as e:
            print(f"[Translation Error] {e}")
            return text  # 翻译失败返回原文

    async def parse_capability_info(
        self,
        name: str,
        description: str,
        metadata: Dict[str, Any],
        use_cache: bool = True,
    ) -> Optional[Dict[str, Any]]:
        """解析 AI 能力信息，支持缓存"""
        # 检查缓存
        if use_cache:
            cache_key = self._generate_cache_key(name, description or "")
            cached = self.cache.get(cache_key)
            if cached:
                print(f"[LLM Cache Hit] {name}")
                return cached

        # 检查 API Key
        if not self.api_key:
            print(f"[LLM Skipped] No API Key configured for {name}")
            return None

        prompt = f"""请分析以下 AI 能力/工具，并提取关键信息：

名称: {name}
描述: {description}
元数据: {json.dumps(metadata, ensure_ascii=False, indent=2)}

请以 JSON 格式返回以下信息：
{{
    "is_open_source": true/false/null (是否开源),
    "key_features": ["特性1", "特性2", ...],
    "pain_points": ["解决的痛点1", "痛点2", ...],
    "differentiation": "与现有方案的主要区别"
}}

如果无法确定，请返回 null。"""

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.api_url}/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": self.model,
                        "messages": [
                            {"role": "system", "content": "你是一个 AI 工具分析专家。请只返回 JSON，不要包含其他文字。"},
                            {"role": "user", "content": prompt},
                        ],
                        "temperature": 0.3,
                    },
                    timeout=60.0,
                )
                response.raise_for_status()
                result = response.json()

                content = result["choices"][0]["message"]["content"]
                # 尝试提取 JSON（可能被 markdown 代码块包裹）
                content = self._extract_json(content)
                parsed = json.loads(content)

                # 存入缓存
                if use_cache and parsed:
                    self.cache.set(cache_key, parsed)

                return parsed

        except json.JSONDecodeError as e:
            print(f"[LLM JSON Error] {name}: {e}")
            return None
        except httpx.HTTPStatusError as e:
            print(f"[LLM HTTP Error] {name}: {e.response.status_code}")
            return None
        except Exception as e:
            print(f"[LLM Error] {name}: {e}")
            return None

    def _extract_json(self, content: str) -> str:
        """从响应中提取 JSON 内容"""
        content = content.strip()
        # 如果被 ```json ... ``` 包裹
        if content.startswith("```"):
            lines = content.split("\n")
            # 移除第一行和最后一行
            if len(lines) > 2:
                content = "\n".join(lines[1:-1])
        return content

    async def parse_with_fallback(
        self,
        name: str,
        description: str,
        metadata: Dict[str, Any],
        use_cache: bool = True,
    ) -> Dict[str, Any]:
        """带降级处理的解析方法"""
        result = await self.parse_capability_info(name, description, metadata, use_cache)

        if result is None:
            return {
                "is_open_source": None,
                "key_features": [],
                "pain_points": [],
                "differentiation": None,
            }

        return {
            "is_open_source": result.get("is_open_source"),
            "key_features": result.get("key_features", []),
            "pain_points": result.get("pain_points", []),
            "differentiation": result.get("differentiation"),
        }

    async def batch_parse(
        self,
        items: List[Dict[str, Any]],
        concurrency: int = 3,
        translate: bool = True,
    ) -> List[Dict[str, Any]]:
        """
        批量解析多个能力
        
        Args:
            items: 待解析的数据列表
            concurrency: 并发数
            translate: 是否翻译描述为中文
        """
        import asyncio
        
        semaphore = asyncio.Semaphore(concurrency)
        results = []

        async def parse_with_semaphore(item: Dict[str, Any]) -> Dict[str, Any]:
            async with semaphore:
                name = item.get("name", "")
                description = item.get("description", "")
                metadata = item.get("metadata_", {})
                
                # 翻译描述为中文
                translated_description = description
                if translate and description:
                    translated_description = await self.translate_to_chinese(description)
                
                # 解析能力信息
                parsed = await self.parse_with_fallback(
                    name=name,
                    description=description,  # 解析时使用原文
                    metadata=metadata,
                )
                
                return {
                    **item,
                    "description": translated_description,  # 存储翻译后的描述
                    "llm_parsed": parsed,
                }

        tasks = [parse_with_semaphore(item) for item in items]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 处理异常结果
        final_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                print(f"[LLM Batch Error] Item {i}: {result}")
                final_results.append({**items[i], "llm_parsed": None})
            else:
                final_results.append(result)

        return final_results


llm_service = LLMService()
