from datetime import datetime, timezone
from fastapi import APIRouter, Response, status

from app.core.config import settings
from app.db.session import ping_db
from app.schemas.health import HealthResponse

router = APIRouter(tags=["Health"])


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="System and Database Health Check",
    description="Validates that the FastAPI service and PostgreSQL database are running and responsive.",
)
def check_health(response: Response) -> HealthResponse:
    is_connected, latency_ms, message = ping_db()

    current_timestamp = datetime.now(timezone.utc)
    if is_connected:
        return HealthResponse(
            status="healthy",
            database="connected",
            database_latency_ms=latency_ms,
            timestamp=current_timestamp,
            environment=settings.ENVIRONMENT,
            version=settings.VERSION,
            message=message,
        )

    # If DB is not reachable, return 503 Service Unavailable
    response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    return HealthResponse(
        status="unhealthy",
        database="disconnected",
        database_latency_ms=latency_ms,
        timestamp=current_timestamp,
        environment=settings.ENVIRONMENT,
        version=settings.VERSION,
        message=f"Database connection error: {message}",
    )
