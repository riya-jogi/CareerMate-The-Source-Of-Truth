from fastapi import APIRouter
from app.api.v1.health import router as health_router
from app.api.v1.auth import router as auth_router
from app.api.v1.dashboard import router as dashboard_router

api_v1_router = APIRouter()

# Register core v1 routers
api_v1_router.include_router(health_router, prefix="", tags=["Health"])
api_v1_router.include_router(auth_router)
api_v1_router.include_router(dashboard_router)

