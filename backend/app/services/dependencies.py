"""Dependency injection providers for FastAPI.

This module provides factory functions for FastAPI's Depends() system,
enabling proper dependency injection and testability.
"""
from typing import Generator, Optional
from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.services.llm_service import LLMService
from app.services.cache_service import CacheService
from app.core.config import settings


def get_db() -> Generator[Session, None, None]:
    """Database session dependency."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_llm_service() -> LLMService:
    """LLM service dependency factory."""
    return LLMService()


def get_cache_service() -> CacheService:
    """Cache service dependency factory."""
    return CacheService()


# Pre-instantiated services for simple cases (backward compatibility)
# These can be replaced with Depends() in API endpoints for testability
_llm_service: Optional[LLMService] = None
_cache_service: Optional[CacheService] = None


def get_llm_service_singleton() -> LLMService:
    """Get or create LLM service singleton."""
    global _llm_service
    if _llm_service is None:
        _llm_service = LLMService()
    return _llm_service


def get_cache_service_singleton() -> CacheService:
    """Get or create cache service singleton."""
    global _cache_service
    if _cache_service is None:
        _cache_service = CacheService()
    return _cache_service
