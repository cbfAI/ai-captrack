from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.collector_service import trigger_collection, get_collection_progress

router = APIRouter()


@router.post("/trigger")
async def trigger_data_collection(
    db: Session = Depends(get_db),
    enable_llm: bool = Query(True, description="是否启用 LLM 智能解析"),
):
    """触发数据采集，可选启用 LLM 智能解析"""
    result = await trigger_collection(db, enable_llm_parsing=enable_llm)
    return result


@router.get("/progress")
def get_progress():
    return get_collection_progress()
