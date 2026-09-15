import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.models.matching import MatchAnalysisStatus, MatchType


class MatchDetailRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    job_requirement_id: uuid.UUID
    career_claim_id: Optional[uuid.UUID]
    match_type: MatchType
    score: float
    explanation: str
    gap_category: Optional[str]
    created_at: datetime
    updated_at: datetime


class CandidateJobMatchRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    career_profile_id: uuid.UUID
    job_id: uuid.UUID
    algorithm_version: str
    overall_score: float
    profile_coverage: float
    required_score: Optional[float]
    preferred_score: Optional[float]
    analysis_status: MatchAnalysisStatus
    critical_gaps: list[str]
    details: list[MatchDetailRead]
    created_at: datetime
    updated_at: datetime