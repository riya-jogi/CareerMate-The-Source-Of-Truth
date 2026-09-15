import uuid
from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


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


class ResumeUploadCreate(BaseModel):
    filename: str = Field(..., min_length=1, max_length=255)
    content_type: str = Field(..., min_length=1, max_length=100)
    content: str = Field(..., min_length=1, max_length=500000)

    @field_validator("filename")
    @classmethod
    def validate_filename(cls, value: str) -> str:
        if "/" in value or "\\" in value:
            raise ValueError("filename must be a simple file name")
        return value.strip()


class ResumeFileRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    career_profile_id: uuid.UUID
    filename: str
    content_type: str
    file_size: int
    status: str
    extracted_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime


class ResumeProposalRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    resume_file_id: uuid.UUID
    proposal_type: ProposalType
    field_name: str
    proposed_value: str
    source_excerpt: Optional[str] = None
    confidence: float
    decision: ProposalDecision
    review_notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class ResumeProposalReview(BaseModel):
    decision: ProposalDecision
    notes: Optional[str] = Field(None, max_length=2000)


class ResumeExtractionResponse(BaseModel):
    resume_id: uuid.UUID
    proposals: list[ResumeProposalRead]
