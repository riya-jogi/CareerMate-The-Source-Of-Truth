import uuid
from pathlib import Path

from fastapi import APIRouter, File, UploadFile, status
from fastapi.responses import FileResponse

from app.api.deps import CurrentUser, DatabaseSession
from app.schemas.resume import (
    ProposalDecision,
    ResumeExtractionResponse,
    ResumeFileRead,
    ResumeProposalRead,
    ResumeProposalReview,
    ResumeUploadCreate,
)
from app.services.resume_service import resume_service
from app.core.config import settings

router = APIRouter(prefix="/resumes", tags=["Resume Upload"])


@router.post("/upload", response_model=ResumeFileRead, status_code=status.HTTP_201_CREATED)
def upload_resume(payload: ResumeUploadCreate, current_user: CurrentUser, db: DatabaseSession):
    resume = resume_service.upload_resume(db, current_user, payload)
    return ResumeFileRead.model_validate(resume)


@router.post("/upload/file", response_model=ResumeFileRead, status_code=status.HTTP_201_CREATED)
def upload_resume_file(file: UploadFile, current_user: CurrentUser, db: DatabaseSession):
    raw_bytes = file.file.read(settings.MAX_RESUME_FILE_SIZE + 1)
    payload = ResumeUploadCreate(
        filename=file.filename or "resume.txt",
        content_type=file.content_type or "application/octet-stream",
        content="uploaded file",
    )
    resume = resume_service.upload_resume(db, current_user, payload, raw_bytes)
    return ResumeFileRead.model_validate(resume)


@router.get("", response_model=list[ResumeFileRead])
def list_resumes(current_user: CurrentUser, db: DatabaseSession):
    resumes = resume_service.list_resumes(db, current_user)
    return [ResumeFileRead.model_validate(item) for item in resumes]


@router.get("/{resume_id}", response_model=ResumeFileRead)
def get_resume(resume_id: uuid.UUID, current_user: CurrentUser, db: DatabaseSession):
    resume = resume_service.get_resume(db, current_user, resume_id)
    return ResumeFileRead.model_validate(resume)


@router.post("/{resume_id}/extract", response_model=ResumeExtractionResponse, status_code=status.HTTP_201_CREATED)
def extract_resume(resume_id: uuid.UUID, current_user: CurrentUser, db: DatabaseSession):
    proposals = resume_service.extract_resume(db, current_user, resume_id)
    return ResumeExtractionResponse(
        resume_id=resume_id,
        proposals=[ResumeProposalRead.model_validate(item) for item in proposals],
    )


@router.get("/{resume_id}/extraction", response_model=ResumeExtractionResponse)
def get_extraction(resume_id: uuid.UUID, current_user: CurrentUser, db: DatabaseSession):
    resume = resume_service.get_resume(db, current_user, resume_id)
    return ResumeExtractionResponse(resume_id=resume_id, proposals=[ResumeProposalRead.model_validate(item) for item in resume.proposals])


@router.get("/{resume_id}/download", response_class=FileResponse)
def download_resume(resume_id: uuid.UUID, current_user: CurrentUser, db: DatabaseSession):
    from app.core.errors import NotFoundError
    resume = resume_service.get_resume(db, current_user, resume_id)
    if not resume.storage_key:
        raise NotFoundError("Stored resume file is not available.")
    path = Path(settings.STORAGE_PATH).resolve() / resume.storage_key
    if not path.is_file():
        raise NotFoundError("Stored resume file is not available.")
    return FileResponse(path, media_type=resume.content_type, filename=resume.filename)


@router.patch("/proposals/{proposal_id}/review", response_model=ResumeProposalRead)
def review_proposal(proposal_id: uuid.UUID, payload: ResumeProposalReview, current_user: CurrentUser, db: DatabaseSession):
    proposal = resume_service.review_proposal(db, current_user, proposal_id, payload)
    return ResumeProposalRead.model_validate(proposal)
