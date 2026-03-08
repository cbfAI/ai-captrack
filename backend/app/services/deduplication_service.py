from typing import List
from sqlalchemy.orm import Session
from app.models.models import AICapability, CapabilitySource
from app.schemas.schemas import AICapabilityCreate
import hashlib


def generate_capability_hash(name: str, source: CapabilitySource) -> str:
    content = f"{name.lower()}:{source.value}"
    return hashlib.md5(content.encode()).hexdigest()


def deduplicate_capabilities(
    db: Session,
    capabilities: List[AICapabilityCreate],
    source: CapabilitySource,
) -> List[AICapability]:
    new_capabilities = []

    for cap in capabilities:
        existing = db.query(AICapability).filter(
            AICapability.name.ilike(cap.name),
            AICapability.source == source,
        ).first()

        if not existing:
            db_cap = AICapability(**cap.model_dump())
            db.add(db_cap)
            new_capabilities.append(db_cap)
        else:
            # 如果数据已存在但描述为空，则更新
            if not existing.description and cap.description:
                existing.description = cap.description
                existing.key_features = cap.key_features or []
                existing.stars = cap.stars
                existing.heat_score = cap.heat_score
                existing.metadata_ = cap.metadata_ or {}
                new_capabilities.append(existing)

    db.commit()
    for cap in new_capabilities:
        db.refresh(cap)

    return new_capabilities
