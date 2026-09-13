from fastapi import APIRouter, status

from app.api.deps import CurrentUser, DatabaseSession
from app.schemas.dashboard import DashboardSummaryResponse
from app.services.dashboard_service import dashboard_service

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get(
    "/summary",
    response_model=DashboardSummaryResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Candidate Dashboard Summary",
    description=(
        "Retrieves real-time dashboard metrics, profile completeness score, "
        "and module status for the authenticated candidate."
    ),
)
def get_dashboard_summary(
    current_user: CurrentUser,
    db: DatabaseSession,
) -> DashboardSummaryResponse:
    return dashboard_service.get_dashboard_summary(db=db, user=current_user)
