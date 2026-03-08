from abc import ABC, abstractmethod
from typing import List
from app.models.models import CapabilitySource
from app.schemas.schemas import AICapabilityCreate


class BaseScraper(ABC):
    source: CapabilitySource

    @abstractmethod
    def collect(self) -> List[AICapabilityCreate]:
        pass
