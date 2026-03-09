from typing import List
import httpx
from app.scrapers.base_scraper import BaseScraper
from app.models.models import CapabilitySource, CapabilityType
from app.schemas.schemas import AICapabilityCreate


class GitHubScraper(BaseScraper):
    source = CapabilitySource.GITHUB

    async def fetch_trending(self) -> List[dict]:
        headers = {"Accept": "application/vnd.github.v3+json"}
        async with httpx.AsyncClient(headers=headers) as client:
            response = await client.get(
                "https://api.github.com/search/repositories",
                params={
                    "q": "ai OR llm OR gpt OR machine-learning",
                    "sort": "stars",
                    "order": "desc",
                    "per_page": 50,
                },
                timeout=30.0,
            )
            response.raise_for_status()
            data = response.json()
            return data.get("items", [])

    def collect(self) -> List[AICapabilityCreate]:
        import asyncio

        try:
            repos = asyncio.get_event_loop().run_until_complete(self.fetch_trending())
        except RuntimeError:
            import asyncio
            repos = asyncio.run(self.fetch_trending())

        capabilities = []
        for repo in repos:
            name = repo.get("full_name", "")
            description = repo.get("description", "") or ""
            language = repo.get("language", "") or ""
            topics = repo.get("topics", [])

            capability_type = CapabilityType.CODE
            if "agent" in topics or "agent" in name.lower():
                capability_type = CapabilityType.AGENT
            elif "model" in topics or "llm" in name.lower():
                capability_type = CapabilityType.MODEL

            license_info = repo.get("license") or {}
            capabilities.append(
                AICapabilityCreate(
                    name=name,
                    description=description,
                    capability_type=capability_type,
                    source=self.source,
                    source_url=repo.get("html_url", ""),
                    is_open_source=license_info.get("spdx_id") is not None,
                    stars=repo.get("stargazers_count", 0),
                    heat_score=repo.get("stargazers_count", 0) * 1.0,
                    metadata_={
                        "language": language,
                        "forks": repo.get("forks_count", 0),
                        "topics": topics,
                    },
                )
            )

        return capabilities
