import uuid
from enum import Enum
from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from app.models.career import CareerClaim
    from app.models.job import Job, JobRequirement
    from app.models.profile import CareerProfile


class MatchType(str, Enum):
    STRONG_MATCH = "strong_match"
    PARTIAL_MATCH = "partial_match"
    GAP = "gap"
    UNKNOWN = "unknown"


class MatchAnalysisStatus(str, Enum):
    COMPLETE = "complete"
    COMPLETE_WITH_GAPS = "complete_with_gaps"
    INCOMPLETE = "incomplete"


class CandidateJobMatch(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "candidate_job_matches"

    career_profile_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("career_profiles.id", ondelete="CASCADE"), index=True, nullable=False)
    job_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("jobs.id", ondelete="CASCADE"), index=True, nullable=False)
    algorithm_version: Mapped[str] = mapped_column(String(50), default="matching-v1", nullable=False)
    overall_score: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)
    profile_coverage: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)
    required_score: Mapped[Optional[float]] = mapped_column(Numeric(5, 2), nullable=True)
    preferred_score: Mapped[Optional[float]] = mapped_column(Numeric(5, 2), nullable=True)
    analysis_status: Mapped[MatchAnalysisStatus] = mapped_column(String(30), nullable=False)
    critical_gaps: Mapped[list] = mapped_column(type_=__import__("sqlalchemy").JSON, default=list, nullable=False)

    career_profile: Mapped["CareerProfile"] = relationship("CareerProfile")
    job: Mapped["Job"] = relationship("Job")
    details: Mapped[list["MatchDetail"]] = relationship("MatchDetail", back_populates="match", cascade="all, delete-orphan")


class MatchDetail(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "match_details"

    match_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("candidate_job_matches.id", ondelete="CASCADE"), index=True, nullable=False)
    job_requirement_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("job_requirements.id", ondelete="CASCADE"), index=True, nullable=False)
    career_claim_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("career_claims.id", ondelete="SET NULL"), nullable=True)
    match_type: Mapped[MatchType] = mapped_column(String(30), nullable=False)
    score: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)
    explanation: Mapped[str] = mapped_column(Text, nullable=False)
    gap_category: Mapped[Optional[str]] = mapped_column(String(40), nullable=True)

    match: Mapped["CandidateJobMatch"] = relationship("CandidateJobMatch", back_populates="details")
    job_requirement: Mapped["JobRequirement"] = relationship("JobRequirement")
    career_claim: Mapped[Optional["CareerClaim"]] = relationship("CareerClaim")