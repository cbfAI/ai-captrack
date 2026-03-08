from typing import List, Optional
import hashlib
import json
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.models import AICapability, UserFeedback
from app.schemas.schemas import (
    AICapabilityResponse,
    AICapabilityCreate,
    AICapabilityUpdate,
    FeedbackCreate,
    FeedbackResponse,
    CapabilitiesFilter,
    PaginatedResponse,
    CapabilityType,
    CapabilitySource,
)
from app.services.capability_service import (
    get_capabilities,
    get_capability_by_id,
    create_capability,
    update_capability,
    delete_capability,
    create_feedback,
    get_capabilities_filtered,
)
from app.services.cache_service import cache_service

router = APIRouter()


@router.get("", response_model=PaginatedResponse)
def list_capabilities(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    capability_type: Optional[CapabilityType] = None,
    source: Optional[CapabilitySource] = None,
    min_stars: Optional[int] = Query(None, ge=0),
    min_heat_score: Optional[float] = Query(None, ge=0),
    search: Optional[str] = None,
    db: Session = Depends(get_db),
):
    filters = CapabilitiesFilter(
        capability_type=capability_type,
        source=source,
        min_stars=min_stars,
        min_heat_score=min_heat_score,
        search=search,
    )

    filters_dict = filters.model_dump() if filters else {}
    filters_hash = hashlib.md5(json.dumps(filters_dict, sort_keys=True).encode()).hexdigest()

    cached_data = cache_service.get_capabilities_cache(page, page_size, filters_hash)
    if cached_data:
        return cached_data

    result = get_capabilities_filtered(db, page, page_size, filters)

    result_dict = {
        "items": [{
            "id": item.id,
            "name": item.name,
            "description": item.description,
            "capability_type": item.capability_type,
            "source": item.source,
            "source_url": item.source_url,
            "is_open_source": item.is_open_source,
            "key_features": item.key_features,
            "pain_points": item.pain_points,
            "differentiation": item.differentiation,
            "stars": item.stars,
            "heat_score": item.heat_score,
            "metadata_": item.metadata_,
            "created_at": item.created_at.isoformat() if item.created_at else None,
            "updated_at": item.updated_at.isoformat() if item.updated_at else None
        } for item in result["items"]],
        "total": result["total"],
        "page": result["page"],
        "page_size": result["page_size"],
        "filters": result["filters"].model_dump() if result["filters"] else None,
    }

    cache_service.set_capabilities_cache(page, page_size, filters_hash, result_dict)

    return result_dict


@router.get("/{capability_id}", response_model=AICapabilityResponse)
def get_capability(capability_id: str, db: Session = Depends(get_db)):
    capability = get_capability_by_id(db, capability_id)
    if not capability:
        raise HTTPException(status_code=404, detail="Capability not found")
    return capability


@router.post("", response_model=AICapabilityResponse)
def create_new_capability(
    capability: AICapabilityCreate, db: Session = Depends(get_db)
):
    cache_service.invalidate_capabilities_cache()
    return create_capability(db, capability)


@router.put("/{capability_id}", response_model=AICapabilityResponse)
def update_capability_by_id(
    capability_id: str,
    capability: AICapabilityUpdate,
    db: Session = Depends(get_db),
):
    cache_service.invalidate_capabilities_cache()
    updated = update_capability(db, capability_id, capability)
    if not updated:
        raise HTTPException(status_code=404, detail="Capability not found")
    return updated


@router.delete("/{capability_id}")
def delete_capability_by_id(capability_id: str, db: Session = Depends(get_db)):
    cache_service.invalidate_capabilities_cache()
    deleted = delete_capability(db, capability_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Capability not found")
    return {"message": "Capability deleted successfully"}


@router.post("/{capability_id}/feedback", response_model=FeedbackResponse)
def submit_feedback(
    capability_id: str, feedback: FeedbackCreate, db: Session = Depends(get_db)
):
    if feedback.capability_id != capability_id:
        raise HTTPException(status_code=400, detail="Capability ID mismatch")
    capability = get_capability_by_id(db, capability_id)
    if not capability:
        raise HTTPException(status_code=404, detail="Capability not found")
    return create_feedback(db, feedback)
