import uuid
from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.models.career import ClaimStatus, ClaimType, EvidenceSource, ExperienceType, Proficiency


class CareerClaimCreate(BaseModel):
    claim_type: ClaimType = ClaimType.SKILL
    claim_text: str = Field(..., min_length=1, max_length=2000)
    subject: str = Field(..., min_length=1, max_length=255)
    context: Optional[str] = Field(None, max_length=2000)
    experience_type: ExperienceType = ExperienceType.PROFESSIONAL
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    proficiency: Optional[Proficiency] = None
    skill_name: Optional[str] = Field(None, max_length=150)

    @model_validator(mode="after")
    def validate_dates(self):
        if self.start_date and self.end_date and self.end_date < self.start_date:
            raise ValueError("end_date must be on or after start_date")
        return self


class CareerClaimRead(CareerClaimCreate):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    status: ClaimStatus
    confidence: float
    candidate_confirmed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime


class CareerClaimUpdate(BaseModel):
    claim_text: Optional[str] = Field(None, min_length=1, max_length=2000)
    subject: Optional[str] = Field(None, min_length=1, max_length=255)
    context: Optional[str] = Field(None, max_length=2000)
    experience_type: Optional[ExperienceType] = None
    proficiency: Optional[Proficiency] = None
    skill_name: Optional[str] = Field(None, max_length=150)


class EvidenceCreate(BaseModel):
    source_type: EvidenceSource = EvidenceSource.CANDIDATE_INPUT
    source_reference: str = Field(..., min_length=1, max_length=255)
    content: str = Field(..., min_length=1, max_length=4000)


class EvidenceRead(EvidenceCreate):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    content_hash: str
    created_at: datetime
    updated_at: datetime


class ClaimEvidenceRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    claim_id: uuid.UUID
    evidence_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
