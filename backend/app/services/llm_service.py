import httpx
import json
import hashlib
from typing import Optional, Dict, Any

from app.core.config import settings


class LLMService:
    def __init__(self):
        self.api_key = settings.LLM_API_KEY
        self.api_url = settings.LLM_API_URL
        self.model = settings.LLM_MODEL

    def _generate_cache_key(self, content: str) -> str:
        return hashlib.md5(content.encode()).hexdigest()

    async def parse_capability_info(
        self,
        name: str,
        description: str,
        metadata: Dict[str, Any],
    ) -> Optional[Dict[str, Any]]:
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
                            {"role": "system", "content": "你是一个 AI 工具分析专家。"},
                            {"role": "user", "content": prompt},
                        ],
                        "temperature": 0.3,
                    },
                    timeout=30.0,
                )
                response.raise_for_status()
                result = response.json()

                content = result["choices"][0]["message"]["content"]
                parsed = json.loads(content)
                return parsed

        except Exception as e:
            print(f"LLM parsing error: {e}")
            return None

    async def parse_with_fallback(
        self,
        name: str,
        description: str,
        metadata: Dict[str, Any],
    ) -> Dict[str, Any]:
        result = await self.parse_capability_info(name, description, metadata)

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


llm_service = LLMService()
