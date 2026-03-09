from typing import List
import httpx
from app.scrapers.base_scraper import BaseScraper
from app.models.models import CapabilitySource, CapabilityType
from app.schemas.schemas import AICapabilityCreate


class OpenRouterScraper(BaseScraper):
    """OpenRouter API 模型采集器"""
    source = CapabilitySource.OPENROUTER

    def fetch_models(self) -> List[dict]:
        """获取 OpenRouter 模型列表"""
        response = httpx.get(
            "https://openrouter.ai/api/v1/models",
            headers={"Accept": "application/json"},
            timeout=30.0,
            follow_redirects=True,
        )
        response.raise_for_status()
        data = response.json()
        return data.get("data", [])

    def collect(self) -> List[AICapabilityCreate]:
        """采集 OpenRouter 模型数据"""
        try:
            models = self.fetch_models()
        except Exception as e:
            print(f"OpenRouter fetch error: {e}")
            return []

        capabilities = []
        for model in models:
            model_id = model.get("id", "")
            name = model.get("name", model_id)
            description = model.get("description", "") or ""
            context_length = model.get("context_length", 0)
            pricing = model.get("pricing", {})
            
            # 根据模型 ID 判断类型
            capability_type = CapabilityType.MODEL
            model_id_lower = model_id.lower()
            if "agent" in model_id_lower:
                capability_type = CapabilityType.AGENT
            elif "code" in model_id_lower or "coder" in model_id_lower:
                capability_type = CapabilityType.CODE

            # 提取关键特性
            key_features = []
            if context_length:
                key_features.append(f"Context: {context_length:,}")
            
            # 模型系列/提供商
            provider = model_id.split("/")[0] if "/" in model_id else "other"
            if provider not in ["other"]:
                key_features.append(f"Provider: {provider}")
            
            # 定价信息
            prompt_price = pricing.get("prompt", "0")
            if prompt_price and float(prompt_price) > 0:
                key_features.append(f"Price: ${float(prompt_price):.6f}/1K tokens")
            elif prompt_price == "0" or prompt_price == 0:
                key_features.append("Free tier available")

            # 构建热度分数（基于模型知名度启发式计算）
            # OpenRouter 没有直接的 stars，我们用启发式规则
            popular_models = ["gpt", "claude", "gemini", "llama", "mistral", "qwen"]
            heat_score = 50.0  # 基础分
            for keyword in popular_models:
                if keyword in model_id_lower:
                    heat_score += 20
                    break
            
            # 长上下文加分
            if context_length and context_length > 100000:
                heat_score += 10

            capabilities.append(
                AICapabilityCreate(
                    name=name,
                    description=description or f"LLM Model: {model_id}",
                    capability_type=capability_type,
                    source=self.source,
                    source_url=f"https://openrouter.ai/models/{model_id}",
                    is_open_source=self._is_open_source(model_id),
                    stars=int(heat_score),  # 使用启发式分数作为 stars
                    heat_score=heat_score,
                    key_features=key_features[:5],
                    metadata_={
                        "model_id": model_id,
                        "context_length": context_length,
                        "pricing": pricing,
                        "provider": provider,
                        "top_provider": model.get("top_provider", {}),
                        "per_request_limits": model.get("per_request_limits", {}),
                    },
                )
            )

        return capabilities

    def _is_open_source(self, model_id: str) -> bool:
        """判断模型是否开源"""
        open_source_keywords = ["llama", "mistral", "qwen", "phi", "gemma", "deepseek", "yi"]
        model_id_lower = model_id.lower()
        return any(kw in model_id_lower for kw in open_source_keywords)
