from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# Production-ready connection pool configuration
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,           # Number of connections to keep in the pool
    max_overflow=20,        # Additional connections allowed beyond pool_size
    pool_timeout=30,        # Seconds to wait before giving up on getting a connection
    pool_recycle=1800,      # Recycle connections after 30 minutes (prevents stale connections)
    connect_args={"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
