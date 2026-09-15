from datetime import date, datetime
from enum import Enum
from typing import TYPE_CHECKING, Optional
import uuid

from sqlalchemy import Date, DateTime, ForeignKey, Numeric, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from app.models.profile import CareerProfile


class ExperienceType(str, Enum):
    PROFESSIONAL = "professional"
    PERSONAL = "personal"
    ACADEMIC = "academic"
    LEARNING = "learning"


class EmploymentType(str, Enum):
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACT = "contract"
    INTERNSHIP = "internship"
    FREELANCE = "freelance"
    OTHER = "other"


class Proficiency(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


class ClaimType(str, Enum):
    SKILL = "skill"
    RESPONSIBILITY = "responsibility"
    ACHIEVEMENT = "achievement"
    PROJECT = "project"
    EXPERIENCE = "experience"
    EDUCATION = "education"
    CERTIFICATION = "certification"


class ClaimStatus(str, Enum):
    EVIDENCE_BACKED = "evidence_backed"
    CANDIDATE_CONFIRMED = "candidate_confirmed"
    SELF_DECLARED = "self_declared"
    NEEDS_CLARIFICATION = "needs_clarification"
    UNSUPPORTED = "unsupported"


class EvidenceSource(str, Enum):
    RESUME = "resume"
    CANDIDATE_INPUT = "candidate_input"
    PROJECT_DESCRIPTION = "project_description"
    EXPERIENCE_DESCRIPTION = "experience_description"
    CERTIFICATION = "certification"
    OTHER = "other"


class Experience(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "experiences"

    career_profile_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("career_profiles.id", ondelete="CASCADE"), index=True, nullable=False
    )
    company_name: Mapped[str] = mapped_column(String(255), nullable=False)
    job_title: Mapped[str] = mapped_column(String(255), nullable=False)
    location: Mapped[Optional[str]] = mapped_column(String(150))
    employment_type: Mapped[EmploymentType] = mapped_column(String(30), default=EmploymentType.FULL_TIME, nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[Optional[date]] = mapped_column(Date)
    is_current: Mapped[bool] = mapped_column(default=False, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)

    career_profile: Mapped["CareerProfile"] = relationship("CareerProfile", back_populates="experiences")


class Project(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "projects"

    career_profile_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("career_profiles.id", ondelete="CASCADE"), index=True, nullable=False
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    role: Mapped[Optional[str]] = mapped_column(String(255))
    project_type: Mapped[ExperienceType] = mapped_column(String(30), default=ExperienceType.PERSONAL, nullable=False)
    start_date: Mapped[Optional[date]] = mapped_column(Date)
    end_date: Mapped[Optional[date]] = mapped_column(Date)
    repository_url: Mapped[Optional[str]] = mapped_column(String(500))
    project_url: Mapped[Optional[str]] = mapped_column(String(500))

    career_profile: Mapped["CareerProfile"] = relationship("CareerProfile", back_populates="projects")


class Education(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "education"

    career_profile_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("career_profiles.id", ondelete="CASCADE"), index=True, nullable=False
    )
    institution: Mapped[str] = mapped_column(String(255), nullable=False)
    degree: Mapped[str] = mapped_column(String(255), nullable=False)
    field_of_study: Mapped[Optional[str]] = mapped_column(String(255))
    start_date: Mapped[Optional[date]] = mapped_column(Date)
    end_date: Mapped[Optional[date]] = mapped_column(Date)
    grade: Mapped[Optional[str]] = mapped_column(String(100))
    description: Mapped[Optional[str]] = mapped_column(Text)

    career_profile: Mapped["CareerProfile"] = relationship("CareerProfile", back_populates="education")


class Certification(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "certifications"

    career_profile_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("career_profiles.id", ondelete="CASCADE"), index=True, nullable=False
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    issuing_organization: Mapped[str] = mapped_column(String(255), nullable=False)
    issue_date: Mapped[Optional[date]] = mapped_column(Date)
    expiry_date: Mapped[Optional[date]] = mapped_column(Date)
    credential_id: Mapped[Optional[str]] = mapped_column(String(255))
    credential_url: Mapped[Optional[str]] = mapped_column(String(500))

    career_profile: Mapped["CareerProfile"] = relationship("CareerProfile", back_populates="certifications")


class Skill(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "skills"

    name: Mapped[str] = mapped_column(String(150), nullable=False)
    normalized_name: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    category: Mapped[Optional[str]] = mapped_column(String(100))

    candidate_skills: Mapped[list["CandidateSkill"]] = relationship("CandidateSkill", back_populates="skill")


class CandidateSkill(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "candidate_skills"
    __table_args__ = (UniqueConstraint("career_profile_id", "skill_id", name="uq_candidate_skill_profile_skill"),)

    career_profile_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("career_profiles.id", ondelete="CASCADE"), index=True, nullable=False
    )
    skill_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("skills.id", ondelete="CASCADE"), index=True, nullable=False
    )
    experience_type: Mapped[ExperienceType] = mapped_column(String(30), default=ExperienceType.PROFESSIONAL, nullable=False)
    proficiency: Mapped[Optional[Proficiency]] = mapped_column(String(30))
    years_used: Mapped[Optional[float]] = mapped_column(Numeric(5, 2))
    first_used: Mapped[Optional[date]] = mapped_column(Date)
    last_used: Mapped[Optional[date]] = mapped_column(Date)

    career_profile: Mapped["CareerProfile"] = relationship("CareerProfile", back_populates="candidate_skills")
    skill: Mapped[Skill] = relationship("Skill", back_populates="candidate_skills")


class CareerClaim(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "career_claims"

    career_profile_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("career_profiles.id", ondelete="CASCADE"), index=True, nullable=False
    )
    claim_type: Mapped[ClaimType] = mapped_column(String(30), nullable=False, default=ClaimType.SKILL)
    claim_text: Mapped[str] = mapped_column(Text, nullable=False)
    subject: Mapped[str] = mapped_column(String(255), nullable=False)
    context: Mapped[Optional[str]] = mapped_column(Text)
    experience_type: Mapped[ExperienceType] = mapped_column(String(30), default=ExperienceType.PROFESSIONAL, nullable=False)
    start_date: Mapped[Optional[date]] = mapped_column(Date)
    end_date: Mapped[Optional[date]] = mapped_column(Date)
    proficiency: Mapped[Optional[Proficiency]] = mapped_column(String(30))
    skill_name: Mapped[Optional[str]] = mapped_column(String(150))
    status: Mapped[ClaimStatus] = mapped_column(String(30), default=ClaimStatus.UNSUPPORTED, nullable=False)
    confidence: Mapped[float] = mapped_column(Numeric(4, 2), default=0.0, nullable=False)
    candidate_confirmed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    career_profile: Mapped["CareerProfile"] = relationship("CareerProfile", back_populates="career_claims")
    evidence_links: Mapped[list["ClaimEvidence"]] = relationship(
        "ClaimEvidence",
        back_populates="career_claim",
        cascade="all, delete-orphan",
    )


class Evidence(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "evidence"

    career_profile_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("career_profiles.id", ondelete="CASCADE"), index=True, nullable=False
    )
    source_type: Mapped[EvidenceSource] = mapped_column(String(30), nullable=False, default=EvidenceSource.CANDIDATE_INPUT)
    source_reference: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    content_hash: Mapped[str] = mapped_column(String(128), nullable=False, index=True)

    career_profile: Mapped["CareerProfile"] = relationship("CareerProfile", back_populates="evidence")
    claim_links: Mapped[list["ClaimEvidence"]] = relationship(
        "ClaimEvidence",
        back_populates="evidence",
        cascade="all, delete-orphan",
    )


class ClaimEvidence(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "claim_evidence"
    __table_args__ = (UniqueConstraint("claim_id", "evidence_id", name="uq_claim_evidence"),)

    claim_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("career_claims.id", ondelete="CASCADE"), index=True, nullable=False
    )
    evidence_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("evidence.id", ondelete="CASCADE"), index=True, nullable=False
    )

    career_claim: Mapped[CareerClaim] = relationship("CareerClaim", back_populates="evidence_links")
    evidence: Mapped[Evidence] = relationship("Evidence", back_populates="claim_links")