from abc import ABC, abstractmethod
from typing import List
from app.models.models import CapabilitySource
from app.schemas.schemas import AICapabilityCreate


class BaseScraper(ABC):
    """Base class for all data scrapers.
    
    All scrapers must implement async collect() method for consistent
    async/await patterns across the codebase.
    """
    source: CapabilitySource

    @abstractmethod
    async def collect(self) -> List[AICapabilityCreate]:
        """Asynchronously collect data from the source.
        
        Returns:
            List of AICapabilityCreate objects.
        """
        pass
