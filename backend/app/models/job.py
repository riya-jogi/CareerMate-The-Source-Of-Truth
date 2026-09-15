import uuid
from enum import Enum
from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from app.models.user import User


class JobAnalysisStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"


class RequirementImportance(str, Enum):
    REQUIRED = "required"
    PREFERRED = "preferred"
    CONTEXTUAL = "contextual"


class RequirementType(str, Enum):
    SKILL = "skill"
    EXPERIENCE = "experience"
    EDUCATION = "education"
    CERTIFICATION = "certification"
    RESPONSIBILITY = "responsibility"
    CONTEXT = "context"


class Job(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "jobs"

    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    title: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    company_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    location: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)
    source: Mapped[str] = mapped_column(String(50), default="manual", nullable=False)
    analysis_status: Mapped[JobAnalysisStatus] = mapped_column(String(30), default=JobAnalysisStatus.PENDING, nullable=False)
    analysis_error: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    user: Mapped["User"] = relationship("User")
    requirements: Mapped[list["JobRequirement"]] = relationship("JobRequirement", back_populates="job", cascade="all, delete-orphan")


class JobRequirement(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "job_requirements"

    job_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("jobs.id", ondelete="CASCADE"), index=True, nullable=False)
    requirement_text: Mapped[str] = mapped_column(Text, nullable=False)
    requirement_type: Mapped[RequirementType] = mapped_column(String(30), default=RequirementType.SKILL, nullable=False)
    importance: Mapped[RequirementImportance] = mapped_column(String(30), default=RequirementImportance.REQUIRED, nullable=False)
    skill_name: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)
    minimum_years: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    experience_type: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)

    job: Mapped["Job"] = relationship("Job", back_populates="requirements")