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

    def _parse_repos(self, repos: List[dict]) -> List[AICapabilityCreate]:
        """解析仓库数据为能力对象"""
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

    async def collect_async(self) -> List[AICapabilityCreate]:
        """异步采集方法"""
        repos = await self.fetch_trending()
        return self._parse_repos(repos)

    def collect(self) -> List[AICapabilityCreate]:
        """同步采集方法（兼容旧接口）"""
        import asyncio
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None
        
        if loop and loop.is_running():
            # 在异步环境中，使用 asyncio.run 会报错
            # 创建一个新的线程来运行
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(asyncio.run, self.collect_async())
                return future.result()
        else:
            return asyncio.run(self.collect_async())
