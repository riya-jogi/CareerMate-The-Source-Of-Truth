import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1.router import api_v1_router
from app.core.config import settings
from app.core.errors import (
    AppException,
    app_exception_handler,
    generic_exception_handler,
    validation_exception_handler,
)
from app.db.session import ping_db

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("careermate")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Check database connection and log system status
    logger.info("Initializing CareerMate Backend...")
    logger.info(f"Environment: {settings.ENVIRONMENT} | Debug: {settings.DEBUG}")
    is_connected, latency_ms, msg = ping_db()
    if is_connected:
        logger.info(f"Database successfully connected ({latency_ms} ms)")
    else:
        logger.warning(f"Database connection warning: {msg}")
    yield
    # Shutdown: Clean up any long-running resources if needed
    logger.info("Shutting down CareerMate Backend...")


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description=settings.PROJECT_DESCRIPTION,
        version=settings.VERSION,
        openapi_url=f"{settings.API_V1_STR}/openapi.json" if settings.DEBUG else None,
        docs_url=f"{settings.API_V1_STR}/docs" if settings.DEBUG else None,
        redoc_url=f"{settings.API_V1_STR}/redoc" if settings.DEBUG else None,
        lifespan=lifespan,
    )

    # 1. CORS Configuration for Frontend
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 2. Global Exception Handlers
    app.add_exception_handler(AppException, app_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, generic_exception_handler)

    # 3. Register API Routers
    app.include_router(api_v1_router, prefix=settings.API_V1_STR)

    # 4. Root Service Metadata Endpoint
    @app.get("/", tags=["System"])
    def root():
        return {
            "name": settings.PROJECT_NAME,
            "version": settings.VERSION,
            "status": "online",
            "docs": f"{settings.API_V1_STR}/docs" if settings.DEBUG else "disabled",
            "health": f"{settings.API_V1_STR}/health",
        }

    # Redirect /docs to /api/v1/docs
    @app.get("/docs", include_in_schema=False)
    def redirect_docs():
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url=f"{settings.API_V1_STR}/docs")

    # Root alias for health
    @app.get("/health", tags=["System"])
    def root_health():
        is_connected, latency_ms, msg = ping_db()
        return {
            "status": "healthy" if is_connected else "unhealthy",
            "database": "connected" if is_connected else "disconnected",
            "database_latency_ms": latency_ms,
        }

    return app


app = create_app()
