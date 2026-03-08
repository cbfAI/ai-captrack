from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.models import AICapability, UserFeedback
from app.schemas.schemas import (
    AICapabilityCreate,
    AICapabilityUpdate,
    FeedbackCreate,
    CapabilitiesFilter,
)


def get_capabilities(db: Session, skip: int = 0, limit: int = 100) -> List[AICapability]:
    return db.query(AICapability).offset(skip).limit(limit).all()


def get_capability_by_id(db: Session, capability_id: str) -> Optional[AICapability]:
    return db.query(AICapability).filter(AICapability.id == capability_id).first()


def get_capabilities_filtered(
    db: Session,
    page: int = 1,
    page_size: int = 20,
    filters: Optional[CapabilitiesFilter] = None,
):
    query = db.query(AICapability)

    if filters:
        if filters.capability_type:
            query = query.filter(AICapability.capability_type == filters.capability_type)
        if filters.source:
            query = query.filter(AICapability.source == filters.source)
        if filters.min_stars is not None:
            query = query.filter(AICapability.stars >= filters.min_stars)
        if filters.min_heat_score is not None:
            query = query.filter(AICapability.heat_score >= filters.min_heat_score)
        if filters.search:
            search_term = f"%{filters.search}%"
            query = query.filter(
                or_(
                    AICapability.name.ilike(search_term),
                    AICapability.description.ilike(search_term),
                )
            )

    total = query.count()
    items = query.offset((page - 1) * page_size).limit(page_size).all()

    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
        "filters": filters,
    }


def create_capability(db: Session, capability: AICapabilityCreate) -> AICapability:
    db_capability = AICapability(**capability.model_dump())
    db.add(db_capability)
    db.commit()
    db.refresh(db_capability)
    return db_capability


def update_capability(
    db: Session, capability_id: str, capability: AICapabilityUpdate
) -> Optional[AICapability]:
    db_capability = get_capability_by_id(db, capability_id)
    if not db_capability:
        return None

    update_data = capability.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_capability, field, value)

    db.commit()
    db.refresh(db_capability)
    return db_capability


def delete_capability(db: Session, capability_id: str) -> bool:
    db_capability = get_capability_by_id(db, capability_id)
    if not db_capability:
        return False
    db.delete(db_capability)
    db.commit()
    return True


def create_feedback(db: Session, feedback: FeedbackCreate) -> UserFeedback:
    db_feedback = UserFeedback(**feedback.model_dump())
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback


def calculate_heat_score(stars: int, feedback_score: float = 0) -> float:
    return stars * 1.0 + feedback_score * 10.0
