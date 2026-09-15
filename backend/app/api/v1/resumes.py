import uuid

from fastapi import APIRouter, status

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

router = APIRouter(prefix="/resumes", tags=["Resume Upload"])


@router.post("/upload", response_model=ResumeFileRead, status_code=status.HTTP_201_CREATED)
def upload_resume(payload: ResumeUploadCreate, current_user: CurrentUser, db: DatabaseSession):
    resume = resume_service.upload_resume(db, current_user, payload)
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


@router.patch("/proposals/{proposal_id}/review", response_model=ResumeProposalRead)
def review_proposal(proposal_id: uuid.UUID, payload: ResumeProposalReview, current_user: CurrentUser, db: DatabaseSession):
    proposal = resume_service.review_proposal(db, current_user, proposal_id, payload.decision, payload.notes)
    return ResumeProposalRead.model_validate(proposal)
