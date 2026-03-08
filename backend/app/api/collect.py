from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.collector_service import trigger_collection, get_collection_progress

router = APIRouter()


@router.post("/trigger")
def trigger_data_collection(db: Session = Depends(get_db)):
    result = trigger_collection(db)
    return result


@router.get("/progress")
def get_progress():
    return get_collection_progress()
