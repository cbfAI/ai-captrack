from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_, desc, asc

from app.models.models import AICapability, UserFeedback, FeedbackType
from app.schemas.schemas import (
    AICapabilityCreate,
    AICapabilityUpdate,
    FeedbackCreate,
    CapabilitiesFilter,
    SortBy,
    SortOrder,
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
        
        # 排序逻辑
        sort_by = filters.sort_by or SortBy.HEAT
        sort_order = filters.sort_order or SortOrder.DESC
        
        # 映射排序字段
        sort_column_map = {
            SortBy.STARS: AICapability.stars,
            SortBy.HEAT: AICapability.heat_score,
            SortBy.NAME: AICapability.name,
            SortBy.CREATED_AT: AICapability.created_at,
            SortBy.UPDATED_AT: AICapability.updated_at,
        }
        
        sort_column = sort_column_map.get(sort_by, AICapability.heat_score)
        
        # 应用排序
        if sort_order == SortOrder.DESC:
            query = query.order_by(desc(sort_column))
        else:
            query = query.order_by(asc(sort_column))

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
    """创建反馈并更新热度"""
    from app.services.heat_score_service import heat_score_service
    
    db_feedback = UserFeedback(**feedback.model_dump())
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    
    # 更新能力的热度分数
    capability = get_capability_by_id(db, feedback.capability_id)
    if capability:
        # 统计反馈
        thumbs_up = db.query(UserFeedback).filter(
            UserFeedback.capability_id == feedback.capability_id,
            UserFeedback.feedback_type == FeedbackType.THUMBS_UP
        ).count()
        thumbs_down = db.query(UserFeedback).filter(
            UserFeedback.capability_id == feedback.capability_id,
            UserFeedback.feedback_type == FeedbackType.THUMBS_DOWN
        ).count()
        
        capability.thumbs_up = thumbs_up
        capability.thumbs_down = thumbs_down
        
        # 计算新热度
        new_heat_score = heat_score_service.update_heat_score(
            capability,
            thumbs_up=thumbs_up,
            thumbs_down=thumbs_down,
        )
        
        # 更新热度趋势
        previous_score = capability.heat_score or 0
        trend = heat_score_service.calculate_trend(new_heat_score, previous_score)
        
        capability.previous_heat_score = previous_score
        capability.heat_score = new_heat_score
        capability.heat_trend = trend
        
        db.commit()
    
    return db_feedback


def update_all_heat_scores(db: Session) -> int:
    """更新所有能力的热度分数"""
    from app.services.heat_score_service import heat_score_service, HeatTrend
    
    capabilities = db.query(AICapability).all()
    updated_count = 0
    
    for cap in capabilities:
        try:
            # 计算新热度
            new_score = heat_score_service.update_heat_score(cap)
            
            # 计算趋势
            previous_score = cap.heat_score or 0
            trend = heat_score_service.calculate_trend(new_score, previous_score)
            
            cap.previous_heat_score = previous_score
            cap.heat_score = new_score
            cap.heat_trend = trend
            updated_count += 1
        except Exception as e:
            print(f"[Heat Score Error] {cap.name}: {e}")
    
    db.commit()
    return updated_count
