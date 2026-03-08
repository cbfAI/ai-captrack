from typing import List
from app.scrapers.base_scraper import BaseScraper
from app.models.models import CapabilitySource, CapabilityType
from app.schemas.schemas import AICapabilityCreate


class MockScraper(BaseScraper):
    source = CapabilitySource.GITHUB

    def collect(self) -> List[AICapabilityCreate]:
        """生成模拟数据用于测试"""
        return [
            AICapabilityCreate(
                name="openai/gpt-4",
                description="Advanced language model from OpenAI",
                capability_type=CapabilityType.MODEL,
                source=self.source,
                source_url="https://github.com/openai/gpt-4",
                is_open_source=False,
                stars=100000,
                heat_score=100000.0,
                metadata_={
                    "language": "Python",
                    "forks": 10000,
                    "topics": ["ai", "llm", "gpt"],
                },
            ),
            AICapabilityCreate(
                name="langchain/langchain",
                description="Framework for developing applications powered by language models",
                capability_type=CapabilityType.AGENT,
                source=self.source,
                source_url="https://github.com/langchain/langchain",
                is_open_source=True,
                stars=80000,
                heat_score=80000.0,
                metadata_={
                    "language": "Python",
                    "forks": 8000,
                    "topics": ["ai", "agent", "framework"],
                },
            ),
            AICapabilityCreate(
                name="huggingface/transformers",
                description="State-of-the-art Machine Learning for JAX, PyTorch and TensorFlow",
                capability_type=CapabilityType.CODE,
                source=CapabilitySource.HUGGINGFACE,
                source_url="https://github.com/huggingface/transformers",
                is_open_source=True,
                stars=70000,
                heat_score=70000.0,
                metadata_={
                    "language": "Python",
                    "forks": 15000,
                    "topics": ["ai", "nlp", "transformers"],
                },
            ),
        ]
