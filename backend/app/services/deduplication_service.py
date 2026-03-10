from typing import List, Dict, Any
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


def update_capability_llm_fields(
    db: Session,
    capability_id: str,
    llm_parsed: Dict[str, Any],
    translated_description: str = None,
) -> AICapability:
    """
    更新能力的 LLM 解析字段
    
    Args:
        db: 数据库会话
        capability_id: 能力ID
        llm_parsed: LLM 解析结果
        translated_description: 翻译后的中文描述（可选）
    """
    capability = db.query(AICapability).filter(
        AICapability.id == capability_id
    ).first()
    
    if not capability:
        raise ValueError(f"Capability not found: {capability_id}")
    
    # 更新翻译后的描述
    if translated_description:
        capability.description = translated_description
    
    # 更新 LLM 解析的字段
    if llm_parsed:
        if llm_parsed.get("is_open_source") is not None:
            capability.is_open_source = llm_parsed["is_open_source"]
        
        if llm_parsed.get("key_features"):
            # 合并已有的 key_features
            existing_features = set(capability.key_features or [])
            new_features = set(llm_parsed["key_features"])
            capability.key_features = list(existing_features | new_features)
        
        if llm_parsed.get("pain_points"):
            # 合并已有的 pain_points
            existing_points = set(capability.pain_points or [])
            new_points = set(llm_parsed["pain_points"])
            capability.pain_points = list(existing_points | new_points)
        
        if llm_parsed.get("differentiation"):
            capability.differentiation = llm_parsed["differentiation"]
    
    db.commit()
    db.refresh(capability)
    
    return capability
