import uuid
from typing import TYPE_CHECKING, Optional
from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from app.models.career import (
        CareerClaim,
        CandidateSkill,
        Certification,
        Education,
        Evidence,
        Experience,
        Project,
    )
    from app.models.resume import ResumeFile
    from app.models.user import User


class CareerProfile(Base, UUIDMixin, TimestampMixin):
    """
    CareerProfile entity: The persistent, candidate-controlled Source of Truth.
    All claims, verified evidence, employment history, and validated resume content
    anchor back to this entity.
    """

    __tablename__ = "career_profiles"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        index=True,
        nullable=False,
    )
    headline: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )
    summary: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    phone: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
    )
    location: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
    )
    linkedin_url: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )
    github_url: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )
    portfolio_url: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )

    experiences: Mapped[list["Experience"]] = relationship(
        "Experience", back_populates="career_profile", cascade="all, delete-orphan"
    )
    projects: Mapped[list["Project"]] = relationship(
        "Project", back_populates="career_profile", cascade="all, delete-orphan"
    )
    education: Mapped[list["Education"]] = relationship(
        "Education", back_populates="career_profile", cascade="all, delete-orphan"
    )
    certifications: Mapped[list["Certification"]] = relationship(
        "Certification", back_populates="career_profile", cascade="all, delete-orphan"
    )
    candidate_skills: Mapped[list["CandidateSkill"]] = relationship(
        "CandidateSkill", back_populates="career_profile", cascade="all, delete-orphan"
    )
    career_claims: Mapped[list["CareerClaim"]] = relationship(
        "CareerClaim", back_populates="career_profile", cascade="all, delete-orphan"
    )
    evidence: Mapped[list["Evidence"]] = relationship(
        "Evidence", back_populates="career_profile", cascade="all, delete-orphan"
    )
    resume_files: Mapped[list["ResumeFile"]] = relationship(
        "ResumeFile", back_populates="career_profile", cascade="all, delete-orphan"
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="career_profile",
    )

    def __repr__(self) -> str:
        return f"<CareerProfile(id={self.id}, user_id={self.user_id}, headline={self.headline})>"
