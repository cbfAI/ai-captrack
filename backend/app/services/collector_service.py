"""Collection service with database-backed job tracking.

Replaces global mutable state with proper database persistence.
All scrapers are called asynchronously for better performance.
"""
from typing import Dict, Any, List, Optional
from datetime import datetime
import logging

from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.models.models import CollectionJob, CollectionJobResult, JobStatus
from app.scrapers.huggingface_scraper import HuggingFaceScraper
from app.scrapers.github_scraper import GitHubScraper
from app.scrapers.futuretools_scraper import FutureToolsScraper
from app.scrapers.mock_scraper import MockScraper
from app.services.deduplication_service import deduplicate_capabilities

logger = logging.getLogger(__name__)


class CollectionService:
    """Service for managing data collection jobs with database persistence."""

    async def trigger_collection(self, db: Session) -> Dict[str, Any]:
        """Start a new collection job.
        
        Creates a job record, runs all scrapers asynchronously,
        and updates progress in real-time.
        """
        # Create new job record
        job = CollectionJob(
            status=JobStatus.RUNNING,
            start_time=datetime.utcnow(),
            total_sources=3,
        )
        db.add(job)
        db.commit()
        db.refresh(job)

        scrapers = [
            HuggingFaceScraper(),
            GitHubScraper(),
            # FutureToolsScraper(),  # Not implemented yet
            # MockScraper(),
        ]

        total_collected = 0
        results: List[Dict[str, Any]] = []

        for i, scraper in enumerate(scrapers):
            # Update progress
            job.current_source = scraper.source.value
            job.current_source_index = i + 1
            job.progress = int((i / len(scrapers)) * 100)
            db.commit()

            try:
                logger.info(f"Collecting from {scraper.source.value}...")
                capabilities = await scraper.collect()

                logger.info(f"Collected {len(capabilities)} items from {scraper.source.value}")
                deduplicated = deduplicate_capabilities(db, capabilities, scraper.source)
                total_collected += len(deduplicated)

                result = CollectionJobResult(
                    job_id=job.id,
                    source=scraper.source.value,
                    collected=len(capabilities),
                    after_dedup=len(deduplicated),
                    status="success",
                )
                db.add(result)
                results.append({
                    "source": scraper.source.value,
                    "collected": len(capabilities),
                    "after_dedup": len(deduplicated),
                    "status": "success",
                })

            except Exception as e:
                logger.error(f"Collection failed for {scraper.source.value}: {e}")
                result = CollectionJobResult(
                    job_id=job.id,
                    source=scraper.source.value,
                    collected=0,
                    after_dedup=0,
                    status="error",
                    error_message=str(e),
                )
                db.add(result)
                results.append({
                    "source": scraper.source.value,
                    "collected": 0,
                    "after_dedup": 0,
                    "status": "error",
                    "error": str(e),
                })

        # Mark job as completed
        job.status = JobStatus.COMPLETED
        job.progress = 100
        job.end_time = datetime.utcnow()
        db.commit()

        return {
            "job_id": job.id,
            "total_collected": total_collected,
            "results": results,
        }

    def get_collection_progress(self, db: Session) -> Dict[str, Any]:
        """Get the progress of the most recent collection job."""
        job = db.query(CollectionJob).order_by(desc(CollectionJob.created_at)).first()
        
        if not job:
            return {
                "status": JobStatus.IDLE.value,
                "current_source": None,
                "progress": 0,
                "total_sources": 3,
                "current_source_index": 0,
                "results": [],
                "start_time": None,
                "end_time": None,
            }

        results = db.query(CollectionJobResult).filter(
            CollectionJobResult.job_id == job.id
        ).all()

        return {
            "status": job.status.value,
            "current_source": job.current_source,
            "progress": job.progress,
            "total_sources": job.total_sources,
            "current_source_index": job.current_source_index,
            "results": [
                {
                    "source": r.source,
                    "collected": r.collected,
                    "after_dedup": r.after_dedup,
                    "status": r.status,
                    "error": r.error_message,
                }
                for r in results
            ],
            "start_time": job.start_time.isoformat() if job.start_time else None,
            "end_time": job.end_time.isoformat() if job.end_time else None,
        }


# For backward compatibility, expose module-level functions
_collection_service = CollectionService()


async def trigger_collection(db: Session) -> Dict[str, Any]:
    """Trigger a new collection job (async wrapper)."""
    return await _collection_service.trigger_collection(db)


def get_collection_progress(db: Session) -> Dict[str, Any]:
    """Get collection progress (sync wrapper)."""
    return _collection_service.get_collection_progress(db)
