import re
import uuid

from sqlalchemy import delete, select
from sqlalchemy.orm import Session, selectinload

from app.core.errors import NotFoundError, ValidationError
from app.models.job import Job, JobAnalysisStatus, JobRequirement, RequirementImportance, RequirementType
from app.models.user import User
from app.schemas.jobs import JobCreate


KNOWN_SKILLS = {
    "python": "Python", "java": "Java", "javascript": "JavaScript", "typescript": "TypeScript",
    "react": "React", "fastapi": "FastAPI", "django": "Django", "flask": "Flask",
    "postgresql": "PostgreSQL", "postgres": "PostgreSQL", "sql": "SQL", "mysql": "MySQL",
    "docker": "Docker", "kubernetes": "Kubernetes", "aws": "AWS", "azure": "Azure", "gcp": "GCP",
    "tensorflow": "TensorFlow", "pytorch": "PyTorch", "git": "Git", "rest api": "REST API",
    "rest apis": "REST API", "restful api": "REST API", "graphql": "GraphQL", "ci/cd": "CI/CD",
}


class JobService:
    @staticmethod
    def _get_job(db: Session, user: User, job_id: uuid.UUID) -> Job:
        job = db.execute(
            select(Job).options(selectinload(Job.requirements)).where(Job.id == job_id, Job.user_id == user.id)
        ).scalar_one_or_none()
        if not job:
            raise NotFoundError("Job was not found.")
        return job

    @staticmethod
    def create_job(db: Session, user: User, payload: JobCreate) -> Job:
        job = Job(user_id=user.id, **payload.model_dump(), analysis_status=JobAnalysisStatus.PENDING)
        db.add(job)
        db.flush()
        return job

    @staticmethod
    def list_jobs(db: Session, user: User) -> list[Job]:
        return db.execute(select(Job).where(Job.user_id == user.id).order_by(Job.created_at.desc())).scalars().all()

    @staticmethod
    def get_job(db: Session, user: User, job_id: uuid.UUID) -> Job:
        return JobService._get_job(db, user, job_id)

    @staticmethod
    def analyze_job(db: Session, user: User, job_id: uuid.UUID) -> Job:
        job = JobService._get_job(db, user, job_id)
        text = job.description
        if not text.strip():
            raise ValidationError("Job description cannot be empty.", {"code": "JD_EMPTY"})
        db.execute(delete(JobRequirement).where(JobRequirement.job_id == job.id))

        lines = [line.strip(" -*\t") for line in text.splitlines() if line.strip()]
        lower_text = text.lower()
        requirements: list[JobRequirement] = []
        seen: set[tuple[str, str]] = set()

        for alias, canonical in KNOWN_SKILLS.items():
            skill_match = re.search(rf"(?<![a-z0-9]){re.escape(alias)}(?![a-z0-9])", lower_text)
            if skill_match:
                clause_start = max(
                    lower_text.rfind(marker, 0, skill_match.start())
                    for marker in (".", "!", "?", "\n", ";")
                ) + 1
                clause_end_candidates = [lower_text.find(marker, skill_match.end()) for marker in (".", "!", "?", "\n", ";")]
                clause_end = min((value for value in clause_end_candidates if value >= 0), default=len(lower_text))
                context_window = lower_text[clause_start:clause_end]
                is_preferred = bool(re.search(r"preferred|nice to have|nice-to-have|bonus|plus|desired", context_window))
                importance = RequirementImportance.PREFERRED if is_preferred else RequirementImportance.REQUIRED
                key = (canonical, importance.value)
                if key not in seen:
                    seen.add(key)
                    requirements.append(JobRequirement(job_id=job.id, requirement_text=f"Experience with {canonical}", skill_name=canonical, requirement_type=RequirementType.SKILL, importance=importance))

        years_match = re.search(r"(?:(\d+)\s*\+?\s*(?:years|yrs)|(?:at least|minimum of)\s*(\d+)\s*years)", lower_text)
        if years_match:
            years = int(next(value for value in years_match.groups() if value))
            requirements.append(JobRequirement(job_id=job.id, requirement_text=years_match.group(0), requirement_type=RequirementType.EXPERIENCE, importance=RequirementImportance.REQUIRED, minimum_years=years, experience_type="professional"))

        if re.search(r"bachelor|master|degree|b\.s\.|b\.tech|m\.s\.|m\.tech", lower_text):
            requirements.append(JobRequirement(job_id=job.id, requirement_text="Relevant degree or educational qualification", requirement_type=RequirementType.EDUCATION, importance=RequirementImportance.REQUIRED))
        if re.search(r"certif|credential", lower_text):
            requirements.append(JobRequirement(job_id=job.id, requirement_text="Relevant certification or credential", requirement_type=RequirementType.CERTIFICATION, importance=RequirementImportance.PREFERRED))
        if not requirements:
            requirements.append(JobRequirement(job_id=job.id, requirement_text=lines[0][:500] if lines else "Job requirements need clarification", requirement_type=RequirementType.CONTEXT, importance=RequirementImportance.CONTEXTUAL))

        db.add_all(requirements)
        job.analysis_status = JobAnalysisStatus.COMPLETED
        job.analysis_error = None
        db.flush()
        db.expire(job, ["requirements"])
        return JobService._get_job(db, user, job.id)


job_service = JobService()