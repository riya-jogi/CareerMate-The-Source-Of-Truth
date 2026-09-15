import uuid

from fastapi import APIRouter, status

from app.api.deps import CurrentUser, DatabaseSession
from app.schemas.jobs import JobAnalysisResponse, JobCreate, JobRead, JobRequirementRead
from app.services.job_service import job_service

router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.post("", response_model=JobRead, status_code=status.HTTP_201_CREATED)
def create_job(payload: JobCreate, current_user: CurrentUser, db: DatabaseSession):
    return job_service.create_job(db, current_user, payload)


@router.get("", response_model=list[JobRead])
def list_jobs(current_user: CurrentUser, db: DatabaseSession):
    return job_service.list_jobs(db, current_user)


@router.get("/{job_id}", response_model=JobRead)
def get_job(job_id: uuid.UUID, current_user: CurrentUser, db: DatabaseSession):
    return job_service.get_job(db, current_user, job_id)


@router.post("/{job_id}/analyze", response_model=JobAnalysisResponse)
def analyze_job(job_id: uuid.UUID, current_user: CurrentUser, db: DatabaseSession):
    job = job_service.analyze_job(db, current_user, job_id)
    return JobAnalysisResponse(job=JobRead.model_validate(job), requirements=[JobRequirementRead.model_validate(item) for item in job.requirements])


@router.get("/{job_id}/requirements", response_model=list[JobRequirementRead])
def list_requirements(job_id: uuid.UUID, current_user: CurrentUser, db: DatabaseSession):
    job = job_service.get_job(db, current_user, job_id)
    return [JobRequirementRead.model_validate(item) for item in job.requirements]