import httpx
import json
import hashlib
import time
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


class LLMService:
    def __init__(self):
        self.api_key = settings.LLM_API_KEY
        self.api_url = settings.LLM_API_URL
        self.model = settings.LLM_MODEL
        self.cache = LLMParseCache(ttl_seconds=settings.CACHE_TTL_LLM_PARSE)

    def _generate_cache_key(self, name: str, description: str) -> str:
        """生成基于名称和描述的缓存键"""
        content = f"{name}:{description}"
        return hashlib.md5(content.encode()).hexdigest()

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
                    f"{self.api_url}/chat/completions",
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
                    timeout=30.0,
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
    ) -> List[Dict[str, Any]]:
        """批量解析多个能力"""
        import asyncio
        
        semaphore = asyncio.Semaphore(concurrency)
        results = []

        async def parse_with_semaphore(item: Dict[str, Any]) -> Dict[str, Any]:
            async with semaphore:
                parsed = await self.parse_with_fallback(
                    name=item.get("name", ""),
                    description=item.get("description", ""),
                    metadata=item.get("metadata_", {}),
                )
                return {**item, "llm_parsed": parsed}

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
