from typing import List
import httpx
from app.scrapers.base_scraper import BaseScraper
from app.models.models import CapabilitySource, CapabilityType
from app.schemas.schemas import AICapabilityCreate


class FutureToolsScraper(BaseScraper):
    source = CapabilitySource.FUTURETOOLS

    async def fetch_tools(self) -> List[dict]:
        """Fetch tools from FutureTools.io (not yet implemented)."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://www.futuretools.io/tools",
                timeout=30.0,
            )
            response.raise_for_status()
            return []

    async def collect(self) -> List[AICapabilityCreate]:
        """Collect AI tools from FutureTools.io (placeholder)."""
        # TODO: Implement actual scraping logic
        return []
