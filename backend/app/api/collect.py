"""Collection API endpoints with async support."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.collector_service import trigger_collection, get_collection_progress

router = APIRouter()


@router.post("/trigger")
async def trigger_data_collection(db: Session = Depends(get_db)):
    """Trigger a new data collection job.
    
    Runs all scrapers asynchronously and returns the collection results.
    """
    result = await trigger_collection(db)
    return result


@router.get("/progress")
def get_progress(db: Session = Depends(get_db)):
    """Get the progress of the most recent collection job."""
    return get_collection_progress(db)
