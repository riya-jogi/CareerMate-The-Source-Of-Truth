from datetime import date, datetime
from typing import Optional
import uuid

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.models.career import EmploymentType, ExperienceType, Proficiency


class ProfileBase(BaseModel):
    headline: Optional[str] = Field(None, max_length=255)
    summary: Optional[str] = None
    phone: Optional[str] = Field(None, max_length=50)
    location: Optional[str] = Field(None, max_length=100)
    linkedin_url: Optional[str] = Field(None, max_length=500)
    github_url: Optional[str] = Field(None, max_length=500)
    portfolio_url: Optional[str] = Field(None, max_length=500)


class ProfileUpdate(ProfileBase):
    pass


class ExperienceCreate(BaseModel):
    company_name: str = Field(..., min_length=1, max_length=255)
    job_title: str = Field(..., min_length=1, max_length=255)
    location: Optional[str] = Field(None, max_length=150)
    employment_type: EmploymentType = EmploymentType.FULL_TIME
    start_date: date
    end_date: Optional[date] = None
    is_current: bool = False
    description: Optional[str] = None

    @model_validator(mode="after")
    def validate_dates(self):
        if self.end_date and self.end_date < self.start_date:
            raise ValueError("end_date must be on or after start_date")
        if self.is_current and self.end_date is not None:
            raise ValueError("current experience cannot have an end_date")
        return self


class ProjectCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: str = Field(..., min_length=1)
    role: Optional[str] = Field(None, max_length=255)
    project_type: ExperienceType = ExperienceType.PERSONAL
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    repository_url: Optional[str] = Field(None, max_length=500)
    project_url: Optional[str] = Field(None, max_length=500)

    @model_validator(mode="after")
    def validate_dates(self):
        if self.start_date and self.end_date and self.end_date < self.start_date:
            raise ValueError("end_date must be on or after start_date")
        return self


class EducationCreate(BaseModel):
    institution: str = Field(..., min_length=1, max_length=255)
    degree: str = Field(..., min_length=1, max_length=255)
    field_of_study: Optional[str] = Field(None, max_length=255)
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    grade: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None

    @model_validator(mode="after")
    def validate_dates(self):
        if self.start_date and self.end_date and self.end_date < self.start_date:
            raise ValueError("end_date must be on or after start_date")
        return self


class CertificationCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    issuing_organization: str = Field(..., min_length=1, max_length=255)
    issue_date: Optional[date] = None
    expiry_date: Optional[date] = None
    credential_id: Optional[str] = Field(None, max_length=255)
    credential_url: Optional[str] = Field(None, max_length=500)

    @model_validator(mode="after")
    def validate_dates(self):
        if self.issue_date and self.expiry_date and self.expiry_date < self.issue_date:
            raise ValueError("expiry_date must be on or after issue_date")
        return self


class CandidateSkillCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=150)
    category: Optional[str] = Field(None, max_length=100)
    experience_type: ExperienceType = ExperienceType.PROFESSIONAL
    proficiency: Optional[Proficiency] = None
    years_used: Optional[float] = Field(None, ge=0, le=100)
    first_used: Optional[date] = None
    last_used: Optional[date] = None

    @model_validator(mode="after")
    def validate_dates(self):
        if self.first_used and self.last_used and self.last_used < self.first_used:
            raise ValueError("last_used must be on or after first_used")
        return self


class ExperienceRead(ExperienceCreate):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class ProjectRead(ProjectCreate):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class EducationRead(EducationCreate):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class CertificationRead(CertificationCreate):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class CandidateSkillRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    name: str
    normalized_name: str
    category: Optional[str]
    experience_type: ExperienceType
    proficiency: Optional[Proficiency]
    years_used: Optional[float]
    first_used: Optional[date]
    last_used: Optional[date]
    created_at: datetime
    updated_at: datetime


class CareerProfileRead(ProfileBase):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    experiences: list[ExperienceRead] = Field(default_factory=list)
    projects: list[ProjectRead] = Field(default_factory=list)
    education: list[EducationRead] = Field(default_factory=list)
    certifications: list[CertificationRead] = Field(default_factory=list)
    skills: list[CandidateSkillRead] = Field(default_factory=list)