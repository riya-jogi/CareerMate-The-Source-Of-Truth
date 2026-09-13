import logging
import time
from typing import Generator, Tuple
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session

from app.core.config import settings

logger = logging.getLogger(__name__)

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=settings.DB_POOL_PRE_PING,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    pool_timeout=settings.DB_POOL_TIMEOUT,
    pool_recycle=1800,
    echo=False,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db() -> Generator[Session, None, None]:
    """
    Database session dependency with automatic transaction lifecycle management.
    Yields a Session, commits on successful completion, rolls back on exception,
    and guarantees session closure.
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def ping_db() -> Tuple[bool, float, str]:
    """
    Health check helper to test database connectivity.
    Returns: (is_connected: bool, latency_ms: float, message: str)
    """
    start_time = time.perf_counter()
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1")).scalar()
            latency_ms = round((time.perf_counter() - start_time) * 1000, 2)
            if result == 1:
                return True, latency_ms, "Database connected and responsive"
            return False, latency_ms, "Unexpected response from database query"
    except Exception as exc:
        latency_ms = round((time.perf_counter() - start_time) * 1000, 2)
        logger.error(f"Database ping failed: {exc}")
        return False, latency_ms, str(exc)
