from typing import List
import httpx
from app.scrapers.base_scraper import BaseScraper
from app.models.models import CapabilitySource, CapabilityType
from app.schemas.schemas import AICapabilityCreate


class FutureToolsScraper(BaseScraper):
    source = CapabilitySource.FUTURETOOLS

    async def fetch_tools(self) -> List[dict]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://www.futuretools.io/tools",
                timeout=30.0,
            )
            response.raise_for_status()
            return []

    def collect(self) -> List[AICapabilityCreate]:
        return []
