from typing import List
import httpx
import re
from app.scrapers.base_scraper import BaseScraper
from app.models.models import CapabilitySource, CapabilityType
from app.schemas.schemas import AICapabilityCreate


class HuggingFaceScraper(BaseScraper):
    source = CapabilitySource.HUGGINGFACE

    def fetch_model_readme(self, model_id: str) -> str:
        """从模型的 README.md 中提取描述"""
        try:
            response = httpx.get(
                f"https://huggingface.co/{model_id}/resolve/main/README.md",
                timeout=10.0,
                follow_redirects=True,
            )
            if response.status_code == 200:
                readme = response.text
                lines = readme.split('\n')
                
                description = ""
                in_description = False
                
                for i, line in enumerate(lines):
                    # 跳过 YAML 元数据部分（以 --- 开头）
                    if i == 0 and line.strip() == '---':
                        continue
                    if i > 0 and line.strip() == '---':
                        continue
                    
                    # 找到第一个非元数据行作为描述开始
                    if i > 0 and line.strip() and not line.startswith('#') and not line.startswith('```'):
                        in_description = True
                        description += line.strip() + " "
                    elif in_description and line.strip():
                        description += line.strip() + " "
                    elif in_description and not line.strip():
                        break
                    
                    if len(description) > 300:
                        break
                
                return description.strip()[:300]
        except Exception:
            pass
        return ""

    def collect(self) -> List[AICapabilityCreate]:
        import httpx

        response = httpx.get(
            "https://huggingface.co/api/models",
            params={"sort": "downloads", "direction": -1, "limit": 50},
            timeout=30.0,
        )
        models = response.json()

        capabilities = []
        
        for model in models:
            model_id = model.get("modelId", "")
            tags = model.get("tags", [])
            downloads = model.get("downloads", 0)
            pipeline_tag = model.get("pipeline_tag", "")

            capability_type = CapabilityType.MODEL
            if "agent" in tags or "agent" in model_id.lower():
                capability_type = CapabilityType.AGENT
            elif "code" in tags or "code" in model_id.lower():
                capability_type = CapabilityType.CODE

            # 尝试从 README 获取描述
            description = self.fetch_model_readme(model_id)
            
            # 如果 README 没有描述，使用 pipeline_tag
            if not description:
                description = pipeline_tag or ""

            capabilities.append(
                AICapabilityCreate(
                    name=model_id,
                    description=description,
                    capability_type=capability_type,
                    source=self.source,
                    source_url=f"https://huggingface.co/{model_id}",
                    is_open_source=True,
                    stars=downloads // 1000,
                    heat_score=downloads / 1000,
                    key_features=tags[:5] if tags else [],
                    metadata_={
                        "downloads": downloads,
                        "likes": model.get("likes", 0),
                        "tags": tags,
                        "pipeline_tag": pipeline_tag,
                    },
                )
            )

        return capabilities
