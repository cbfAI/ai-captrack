import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, Integer, Float, Boolean, Enum, JSON, DateTime

from app.db.database import Base
import enum


class CapabilityType(str, enum.Enum):
    AGENT = "Agent"
    CODE = "Code"
    MODEL = "Model"


class CapabilitySource(str, enum.Enum):
    HUGGINGFACE = "huggingface"
    GITHUB = "github"
    FUTURETOOLS = "futuretools"


class FeedbackType(str, enum.Enum):
    THUMBS_UP = "thumbs_up"
    THUMBS_DOWN = "thumbs_down"


class AICapability(Base):
    __tablename__ = "ai_capabilities"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    capability_type = Column(Enum(CapabilityType), nullable=False, index=True)
    source = Column(Enum(CapabilitySource), nullable=False)
    source_url = Column(String(500))
    is_open_source = Column(Boolean, default=None)
    key_features = Column(JSON, default=list)
    pain_points = Column(JSON, default=list)
    differentiation = Column(Text)
    stars = Column(Integer, default=0)
    heat_score = Column(Float, default=0.0, index=True)
    metadata_ = Column("metadata", JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class UserFeedback(Base):
    __tablename__ = "user_feedbacks"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    capability_id = Column(String(36), nullable=False, index=True)
    feedback_type = Column(Enum(FeedbackType), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class UserFavorite(Base):
    __tablename__ = "user_favorites"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    capability_id = Column(String(36), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class JobStatus(str, enum.Enum):
    IDLE = "idle"
    RUNNING = "running"
    COMPLETED = "completed"
    ERROR = "error"


class CollectionJob(Base):
    """Database-backed job tracking to replace global mutable state."""
    __tablename__ = "collection_jobs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    status = Column(Enum(JobStatus), default=JobStatus.IDLE, index=True)
    current_source = Column(String(50))
    progress = Column(Integer, default=0)
    total_sources = Column(Integer, default=3)
    current_source_index = Column(Integer, default=0)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class CollectionJobResult(Base):
    """Per-source results for a collection job."""
    __tablename__ = "collection_job_results"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    job_id = Column(String(36), nullable=False, index=True)
    source = Column(String(50), nullable=False)
    collected = Column(Integer, default=0)
    after_dedup = Column(Integer, default=0)
    status = Column(String(20), default="success")
    error_message = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
