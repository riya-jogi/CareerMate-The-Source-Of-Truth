from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class DashboardSummaryResponse(BaseModel):
    """Real-time dashboard metrics and profile progress for the candidate."""

    candidate_name: str = Field(..., description="Candidate's full name")
    candidate_email: str = Field(..., description="Candidate's account email")
    candidate_headline: Optional[str] = Field(None, description="Current professional headline")
    profile_completeness_percentage: int = Field(
        ...,
        ge=0,
        le=100,
        description="Calculated profile completeness based on anchored profile fields",
    )
    career_claims_count: int = Field(
        default=0,
        ge=0,
        description="Number of verified factual career claims anchored in the profile",
    )
    evidence_sources_count: int = Field(
        default=0,
        ge=0,
        description="Number of uploaded proof documents, resumes, and certificates",
    )
    analyzed_jobs_count: int = Field(
        default=0,
        ge=0,
        description="Number of parsed target job descriptions",
    )
    optimized_resumes_count: int = Field(
        default=0,
        ge=0,
        description="Number of truth-validated optimized resumes generated",
    )
    target_matches_count: int = Field(
        default=0,
        ge=0,
        description="Number of candidate-to-job compatibility evaluations conducted",
    )
    active_anchor: bool = Field(
        default=True,
        description="Whether the candidate's CareerProfile anchor is established",
    )
    account_created_at: datetime = Field(..., description="Timestamp of account creation")
    last_login_at: Optional[datetime] = Field(None, description="Timestamp of last login")
