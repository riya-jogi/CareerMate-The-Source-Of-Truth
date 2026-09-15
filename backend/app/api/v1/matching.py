import uuid

from fastapi import APIRouter

from app.api.deps import CurrentUser, DatabaseSession
from app.schemas.matching import CandidateJobMatchRead
from app.services.matching_service import matching_service

router = APIRouter(prefix="/jobs", tags=["Matching"])


@router.post("/{job_id}/match", response_model=CandidateJobMatchRead)
def match_job(job_id: uuid.UUID, current_user: CurrentUser, db: DatabaseSession):
    return matching_service.run_match(db, current_user, job_id)


@router.get("/{job_id}/match", response_model=CandidateJobMatchRead)
def get_match(job_id: uuid.UUID, current_user: CurrentUser, db: DatabaseSession):
    from sqlalchemy import select
    from sqlalchemy.orm import selectinload
    from app.core.errors import NotFoundError
    from app.models.job import Job
    from app.models.profile import CareerProfile
    from app.models.matching import CandidateJobMatch

    job = db.execute(select(Job).where(Job.id == job_id, Job.user_id == current_user.id)).scalar_one_or_none()
    if not job:
        raise NotFoundError("Job was not found.")
    profile = db.execute(select(CareerProfile).where(CareerProfile.user_id == current_user.id)).scalar_one_or_none()
    result = db.execute(select(CandidateJobMatch).options(selectinload(CandidateJobMatch.details)).where(CandidateJobMatch.job_id == job_id, CandidateJobMatch.career_profile_id == profile.id if profile else None)).scalars().first()
    if not result:
        raise NotFoundError("No match analysis exists for this job.")
    return result