import uuid
from enum import Enum
from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, JSON, Integer, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from app.models.career import CareerClaim
    from app.models.job import Job
    from app.models.profile import CareerProfile
    from app.models.resume import ResumeFile


class ResumeVersionStatus(str, Enum):
    DRAFT = "draft"
    PENDING_REVIEW = "pending_review"
    APPROVED = "approved"
    READY = "ready"
    NEEDS_REVIEW = "needs_review"
    FAILED = "failed"


class ChangeType(str, Enum):
    ADD = "add"
    REMOVE = "remove"
    REWRITE = "rewrite"
    REORDER = "reorder"
    CONDENSE = "condense"
    NORMALIZE = "normalize"


class ValidationStatus(str, Enum):
    PASS = "pass"
    WARNING = "warning"
    BLOCK = "block"
    NEEDS_CLARIFICATION = "needs_clarification"


class ApprovalDecision(str, Enum):
    APPROVED = "approved"
    REJECTED = "rejected"
    EDITED = "edited"


class Resume(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "resumes"

    career_profile_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("career_profiles.id", ondelete="CASCADE"), index=True, nullable=False)
    original_file_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("resume_files.id", ondelete="SET NULL"), nullable=True)
    name: Mapped[str] = mapped_column(String(255), default="Master Resume", nullable=False)

    career_profile: Mapped["CareerProfile"] = relationship("CareerProfile")
    original_file: Mapped[Optional["ResumeFile"]] = relationship("ResumeFile")
    versions: Mapped[list["ResumeVersion"]] = relationship("ResumeVersion", back_populates="resume", cascade="all, delete-orphan")


class ResumeVersion(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "resume_versions"

    resume_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("resumes.id", ondelete="CASCADE"), index=True, nullable=False)
    job_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("jobs.id", ondelete="SET NULL"), index=True, nullable=True)
    version_number: Mapped[int] = mapped_column(Integer, nullable=False)
    content_snapshot: Mapped[dict] = mapped_column(JSON, nullable=False)
    template: Mapped[str] = mapped_column(String(50), default="professional_ats", nullable=False)
    status: Mapped[ResumeVersionStatus] = mapped_column(String(30), default=ResumeVersionStatus.PENDING_REVIEW, nullable=False)
    validation_status: Mapped[ValidationStatus] = mapped_column(String(30), default=ValidationStatus.PASS, nullable=False)
    pdf_key: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    docx_key: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    pdf_checksum: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    docx_checksum: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)

    resume: Mapped["Resume"] = relationship("Resume", back_populates="versions")
    job: Mapped[Optional["Job"]] = relationship("Job")
    changes: Mapped[list["ResumeChange"]] = relationship("ResumeChange", back_populates="version", cascade="all, delete-orphan")


class ResumeChange(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "resume_changes"

    resume_version_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("resume_versions.id", ondelete="CASCADE"), index=True, nullable=False)
    change_type: Mapped[ChangeType] = mapped_column(String(30), nullable=False)
    section: Mapped[str] = mapped_column(String(50), nullable=False)
    original_content: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    proposed_content: Mapped[str] = mapped_column(Text, nullable=False)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    risk_level: Mapped[str] = mapped_column(String(20), default="low", nullable=False)
    validation_status: Mapped[ValidationStatus] = mapped_column(String(30), nullable=False)
    primary_claim_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("career_claims.id", ondelete="SET NULL"), nullable=True)

    version: Mapped["ResumeVersion"] = relationship("ResumeVersion", back_populates="changes")
    primary_claim: Mapped[Optional["CareerClaim"]] = relationship("CareerClaim")
    approval: Mapped[Optional["Approval"]] = relationship("Approval", back_populates="change", uselist=False, cascade="all, delete-orphan")


class Approval(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "approvals"

    resume_change_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("resume_changes.id", ondelete="CASCADE"), unique=True, nullable=False)
    decision: Mapped[ApprovalDecision] = mapped_column(String(30), nullable=False)
    edited_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    candidate_comment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    change: Mapped["ResumeChange"] = relationship("ResumeChange", back_populates="approval")