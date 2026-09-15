import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.models.job import JobAnalysisStatus, RequirementImportance, RequirementType


class JobCreate(BaseModel):
    title: Optional[str] = Field(None, max_length=255)
    company_name: Optional[str] = Field(None, max_length=255)
    description: str = Field(..., min_length=20, max_length=100000)
    location: Optional[str] = Field(None, max_length=150)


class JobRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    title: Optional[str]
    company_name: Optional[str]
    description: str
    location: Optional[str]
    source: str
    analysis_status: JobAnalysisStatus
    analysis_error: Optional[str]
    created_at: datetime
    updated_at: datetime


class JobRequirementRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    job_id: uuid.UUID
    requirement_text: str
    requirement_type: RequirementType
    importance: RequirementImportance
    skill_name: Optional[str]
    minimum_years: Optional[int]
    experience_type: Optional[str]
    created_at: datetime
    updated_at: datetime


class JobAnalysisResponse(BaseModel):
    job: JobRead
    requirements: list[JobRequirementRead]