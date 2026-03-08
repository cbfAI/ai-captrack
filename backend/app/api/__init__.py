from fastapi import APIRouter
from app.api import capabilities, collect, favorites

api_router = APIRouter()

api_router.include_router(capabilities.router, prefix="/capabilities", tags=["capabilities"])
api_router.include_router(collect.router, prefix="/collect", tags=["collect"])
api_router.include_router(favorites.router, prefix="", tags=["favorites"])
