import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.models.resume_version import ApprovalDecision, ChangeType, ResumeVersionStatus, ValidationStatus


class OptimizeRequest(BaseModel):
    template: str = Field("professional_ats", pattern=r"^(professional_ats|modern_ats|compact_ats)$")


class ApprovalRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    resume_change_id: uuid.UUID
    decision: ApprovalDecision
    edited_text: Optional[str]
    candidate_comment: Optional[str]
    created_at: datetime
    updated_at: datetime


class ChangeRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    resume_version_id: uuid.UUID
    change_type: ChangeType
    section: str
    original_content: Optional[str]
    proposed_content: str
    reason: str
    risk_level: str
    validation_status: ValidationStatus
    primary_claim_id: Optional[uuid.UUID]
    approval: Optional[ApprovalRead] = None
    created_at: datetime
    updated_at: datetime


class ResumeVersionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    resume_id: uuid.UUID
    job_id: Optional[uuid.UUID]
    version_number: int
    content_snapshot: dict
    template: str
    status: ResumeVersionStatus
    validation_status: ValidationStatus
    pdf_key: Optional[str]
    docx_key: Optional[str]
    created_at: datetime
    updated_at: datetime
    changes: list[ChangeRead] = Field(default_factory=list)


class ChangeDecision(BaseModel):
    decision: str = Field(..., pattern=r"^(approved|rejected|edited)$")
    edited_text: Optional[str] = Field(None, max_length=10000)
    candidate_comment: Optional[str] = Field(None, max_length=2000)


class GenerateRequest(BaseModel):
    format: str = Field("pdf", pattern=r"^(pdf|docx)$")


class QualityRead(BaseModel):
    status: str
    checks: dict[str, str]
    issues: list[str] = Field(default_factory=list)
