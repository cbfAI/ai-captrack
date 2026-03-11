from typing import Optional, List, Any
from uuid import UUID
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, field_validator
from app.models.models import CapabilityType, CapabilitySource, FeedbackType, HeatTrend


class AICapabilityBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    capability_type: CapabilityType
    source: CapabilitySource
    source_url: Optional[str] = Field(None, max_length=500)
    is_open_source: Optional[bool] = None
    key_features: List[str] = Field(default_factory=list)
    pain_points: List[str] = Field(default_factory=list)
    differentiation: Optional[str] = None
    stars: int = Field(default=0)
    heat_score: float = Field(default=0.0)
    metadata_: dict = Field(alias="metadata", default_factory=dict)


class AICapabilityCreate(AICapabilityBase):
    pass


class AICapabilityUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    capability_type: Optional[CapabilityType] = None
    source_url: Optional[str] = Field(None, max_length=500)
    is_open_source: Optional[bool] = None
    key_features: Optional[List[str]] = None
    pain_points: Optional[List[str]] = None
    differentiation: Optional[str] = None
    stars: Optional[int] = None
    heat_score: Optional[float] = None
    metadata_: Optional[dict] = Field(alias="metadata", default=None)


class AICapabilityResponse(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    translated_description: Optional[str] = None
    capability_type: str
    source: str
    source_url: Optional[str] = None
    is_open_source: Optional[bool] = None
    key_features: List[str] = Field(default_factory=list)
    pain_points: List[str] = Field(default_factory=list)
    differentiation: Optional[str] = None
    stars: int = Field(default=0)
    heat_score: float = Field(default=0.0)
    heat_trend: Optional[str] = None
    thumbs_up: int = Field(default=0)
    thumbs_down: int = Field(default=0)
    metadata_: dict = Field(default_factory=dict)
    created_at: datetime
    updated_at: datetime
    
    @field_validator('heat_trend', mode='before')
    @classmethod
    def convert_heat_trend(cls, v):
        if hasattr(v, 'value'):
            return v.value
        return v

    class Config:
        from_attributes = True
        populate_by_name = True


class FeedbackCreate(BaseModel):
    capability_id: str
    feedback_type: FeedbackType


class FeedbackResponse(BaseModel):
    id: str
    capability_id: str
    feedback_type: FeedbackType
    created_at: datetime

    class Config:
        from_attributes = True


class FavoriteCreate(BaseModel):
    capability_id: str


class FavoriteResponse(BaseModel):
    id: str
    capability_id: str
    created_at: datetime

    class Config:
        from_attributes = True


class StatisticsResponse(BaseModel):
    total: int
    by_type: dict
    by_source: dict
    avg_stars: float
    avg_heat_score: float


class SortBy(str, Enum):
    STARS = "stars"
    HEAT = "heat"
    NAME = "name"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"


class SortOrder(str, Enum):
    ASC = "asc"
    DESC = "desc"


class CapabilitiesFilter(BaseModel):
    capability_type: Optional[CapabilityType] = None
    source: Optional[CapabilitySource] = None
    min_stars: Optional[int] = Field(None, ge=0)
    min_heat_score: Optional[float] = Field(None, ge=0)
    search: Optional[str] = None
    sort_by: Optional[SortBy] = SortBy.HEAT
    sort_order: Optional[SortOrder] = SortOrder.DESC


class PaginatedResponse(BaseModel):
    items: List[AICapabilityResponse]
    total: int
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)
    filters: Optional[CapabilitiesFilter] = None
