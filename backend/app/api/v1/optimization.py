import uuid
from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import FileResponse

from app.api.deps import CurrentUser, DatabaseSession
from app.core.config import settings
from app.schemas.optimization import ChangeDecision, ChangeRead, GenerateRequest, OptimizeRequest, QualityRead, ResumeVersionRead
from app.services.resume_generation_service import resume_generation_service

router = APIRouter(prefix="/jobs", tags=["Resume Optimization"])


@router.post("/{job_id}/optimize", response_model=ResumeVersionRead)
def optimize_job(job_id: uuid.UUID, payload: OptimizeRequest, current_user: CurrentUser, db: DatabaseSession):
    return resume_generation_service.optimize(db, current_user, job_id, payload.template)


@router.get("/{job_id}/optimization", response_model=ResumeVersionRead)
def get_optimization(job_id: uuid.UUID, current_user: CurrentUser, db: DatabaseSession):
    from sqlalchemy import select
    from sqlalchemy.orm import selectinload
    from app.core.errors import NotFoundError
    from app.models.resume_version import ResumeChange, ResumeVersion
    from app.models.profile import CareerProfile
    profile = db.execute(select(CareerProfile).where(CareerProfile.user_id == current_user.id)).scalar_one_or_none()
    version = db.execute(
        select(ResumeVersion)
        .options(selectinload(ResumeVersion.changes).selectinload(ResumeChange.approval))
        .join(ResumeVersion.resume)
        .where(ResumeVersion.job_id == job_id, ResumeVersion.resume.has(career_profile_id=profile.id if profile else None))
        .order_by(ResumeVersion.created_at.desc())
    ).scalars().first()
    if not version:
        raise NotFoundError("No optimization proposal exists for this job.")
    return version


@router.get("/optimizations/{version_id}/changes", response_model=list[ChangeRead])
def get_changes(version_id: uuid.UUID, current_user: CurrentUser, db: DatabaseSession):
    from sqlalchemy import select
    from app.core.errors import NotFoundError
    from app.models.resume_version import Resume, ResumeChange, ResumeVersion
    from app.models.profile import CareerProfile
    changes = db.execute(
        select(ResumeChange)
        .join(ResumeChange.version)
        .join(ResumeVersion.resume)
        .where(ResumeChange.resume_version_id == version_id, Resume.career_profile_id == db.execute(select(CareerProfile.id).where(CareerProfile.user_id == current_user.id)).scalar_one_or_none())
    ).scalars().all()
    if not changes:
        version_exists = db.execute(select(ResumeVersion.id).where(ResumeVersion.id == version_id)).scalar_one_or_none()
        if not version_exists:
            raise NotFoundError("Resume optimization was not found.")
    return changes


@router.post("/changes/{change_id}/decision", response_model=ChangeRead)
def decide_change(change_id: uuid.UUID, payload: ChangeDecision, current_user: CurrentUser, db: DatabaseSession):
    return resume_generation_service.decide_change(db, current_user, change_id, payload.decision, payload.edited_text, payload.candidate_comment)


@router.post("/{job_id}/resume/generate", response_model=ResumeVersionRead)
def generate_resume(job_id: uuid.UUID, payload: GenerateRequest, current_user: CurrentUser, db: DatabaseSession):
    from sqlalchemy import select
    from app.core.errors import NotFoundError
    from app.models.resume_version import ResumeVersion
    from app.models.profile import CareerProfile
    profile = db.execute(select(CareerProfile).where(CareerProfile.user_id == current_user.id)).scalar_one_or_none()
    version = db.execute(select(ResumeVersion).join(ResumeVersion.resume).where(ResumeVersion.job_id == job_id, ResumeVersion.resume.has(career_profile_id=profile.id if profile else None)).order_by(ResumeVersion.created_at.desc())).scalars().first()
    if not version:
        raise NotFoundError("No optimization version exists for this job.")
    generated, _ = resume_generation_service.generate(db, current_user, version.id, payload.format)
    return generated


@router.get("/resume-versions/{version_id}/download")
def download_resume(version_id: uuid.UUID, format: str, current_user: CurrentUser, db: DatabaseSession):
    from sqlalchemy import select
    from app.core.errors import NotFoundError, ValidationError
    from app.models.resume_version import ResumeVersion
    from app.models.profile import CareerProfile
    if format not in {"pdf", "docx"}:
        raise ValidationError("Format must be pdf or docx.")
    profile = db.execute(select(CareerProfile).where(CareerProfile.user_id == current_user.id)).scalar_one_or_none()
    version = db.execute(select(ResumeVersion).join(ResumeVersion.resume).where(ResumeVersion.id == version_id, ResumeVersion.resume.has(career_profile_id=profile.id if profile else None))).scalar_one_or_none()
    if not version:
        raise NotFoundError("Resume version was not found.")
    key = version.pdf_key if format == "pdf" else version.docx_key
    if not key:
        raise NotFoundError("This format has not been generated for the version.")
    path = Path(settings.STORAGE_PATH).resolve() / key
    if not path.is_file():
        raise NotFoundError("Generated resume file is unavailable.")
    return FileResponse(path, media_type="application/pdf" if format == "pdf" else "application/vnd.openxmlformats-officedocument.wordprocessingml.document", filename=path.name)


@router.get("/resume-versions/{version_id}/quality", response_model=QualityRead)
def resume_quality(version_id: uuid.UUID, current_user: CurrentUser, db: DatabaseSession):
    from sqlalchemy import select
    from app.core.errors import NotFoundError
    from app.models.resume_version import ResumeVersion
    from app.models.profile import CareerProfile
    profile = db.execute(select(CareerProfile).where(CareerProfile.user_id == current_user.id)).scalar_one_or_none()
    version = db.execute(select(ResumeVersion).join(ResumeVersion.resume).where(ResumeVersion.id == version_id, ResumeVersion.resume.has(career_profile_id=profile.id if profile else None))).scalar_one_or_none()
    if not version:
        raise NotFoundError("Resume version was not found.")
    return resume_generation_service.validate_document(__import__("app.resume_generation_document", fromlist=["ResumeDocument"]).ResumeDocument.model_validate(version.content_snapshot))