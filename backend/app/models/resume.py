import uuid
from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Optional

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from app.models.profile import CareerProfile


class ProposalType(str, Enum):
    SKILL = "skill"
    EXPERIENCE = "experience"
    EDUCATION = "education"
    CERTIFICATION = "certification"
    PROJECT = "project"
    SUMMARY = "summary"


class ProposalDecision(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class ResumeFile(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "resume_files"

    career_profile_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("career_profiles.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    content_type: Mapped[str] = mapped_column(String(100), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    storage_key: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    checksum: Mapped[Optional[str]] = mapped_column(String(64), nullable=True, index=True)
    file_size: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    status: Mapped[str] = mapped_column(String(30), default="uploaded", nullable=False)
    extracted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    career_profile: Mapped["CareerProfile"] = relationship("CareerProfile", back_populates="resume_files")
    proposals: Mapped[list["ResumeProposal"]] = relationship(
        "ResumeProposal",
        back_populates="resume_file",
        cascade="all, delete-orphan",
    )


class ResumeProposal(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "resume_proposals"

    resume_file_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("resume_files.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    proposal_type: Mapped[ProposalType] = mapped_column(String(30), nullable=False)
    field_name: Mapped[str] = mapped_column(String(100), nullable=False)
    proposed_value: Mapped[str] = mapped_column(Text, nullable=False)
    source_excerpt: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    confidence: Mapped[float] = mapped_column(Numeric(4, 2), default=0.0, nullable=False)
    decision: Mapped[ProposalDecision] = mapped_column(String(30), default=ProposalDecision.PENDING, nullable=False)
    review_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    resume_file: Mapped[ResumeFile] = relationship("ResumeFile", back_populates="proposals")
