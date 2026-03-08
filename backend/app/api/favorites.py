from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db.database import get_db
from app.models.models import AICapability, UserFavorite, UserFeedback
from app.schemas.schemas import FavoriteCreate, FavoriteResponse, StatisticsResponse

router = APIRouter()


@router.post("/favorites", response_model=FavoriteResponse)
def add_favorite(favorite: FavoriteCreate, db: Session = Depends(get_db)):
    existing = db.query(UserFavorite).filter(
        UserFavorite.capability_id == favorite.capability_id
    ).first()
    
    if existing:
        return existing
    
    db_favorite = UserFavorite(capability_id=favorite.capability_id)
    db.add(db_favorite)
    db.commit()
    db.refresh(db_favorite)
    return db_favorite


@router.delete("/favorites/{capability_id}")
def remove_favorite(capability_id: str, db: Session = Depends(get_db)):
    favorite = db.query(UserFavorite).filter(
        UserFavorite.capability_id == capability_id
    ).first()
    
    if favorite:
        db.delete(favorite)
        db.commit()
        return {"message": "Favorite removed successfully"}
    
    return {"message": "Favorite not found"}


@router.get("/favorites", response_model=list[FavoriteResponse])
def get_favorites(db: Session = Depends(get_db)):
    favorites = db.query(UserFavorite).all()
    return favorites


@router.get("/statistics", response_model=StatisticsResponse)
def get_statistics(db: Session = Depends(get_db)):
    total = db.query(AICapability).count()
    
    by_type = {}
    for cap_type in db.query(AICapability.capability_type, func.count(AICapability.id)).group_by(AICapability.capability_type).all():
        by_type[cap_type[0].value if hasattr(cap_type[0], 'value') else str(cap_type[0])] = cap_type[1]
    
    by_source = {}
    for source in db.query(AICapability.source, func.count(AICapability.id)).group_by(AICapability.source).all():
        by_source[source[0].value if hasattr(source[0], 'value') else str(source[0])] = source[1]
    
    avg_stars = db.query(func.avg(AICapability.stars)).scalar() or 0
    avg_heat_score = db.query(func.avg(AICapability.heat_score)).scalar() or 0
    
    return {
        "total": total,
        "by_type": by_type,
        "by_source": by_source,
        "avg_stars": float(avg_stars),
        "avg_heat_score": float(avg_heat_score),
    }
