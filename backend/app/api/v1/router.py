from fastapi import APIRouter
from app.api.v1.health import router as health_router
from app.api.v1.auth import router as auth_router
from app.api.v1.dashboard import router as dashboard_router
from app.api.v1.profile import router as profile_router
from app.api.v1.claims import router as claims_router
from app.api.v1.resumes import router as resumes_router
from app.api.v1.jobs import router as jobs_router
from app.api.v1.matching import router as matching_router

api_v1_router = APIRouter()

# Register core v1 routers
api_v1_router.include_router(health_router, prefix="", tags=["Health"])
api_v1_router.include_router(auth_router)
api_v1_router.include_router(dashboard_router)
api_v1_router.include_router(profile_router)
api_v1_router.include_router(claims_router)
api_v1_router.include_router(resumes_router)
api_v1_router.include_router(jobs_router)
api_v1_router.include_router(matching_router)

