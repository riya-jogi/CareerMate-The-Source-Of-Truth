from datetime import date
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class ResumeHeader(BaseModel):
    name: str
    headline: Optional[str] = None
    email: str
    phone: Optional[str] = None
    location: Optional[str] = None
    links: list[str] = Field(default_factory=list)


class ResumeExperience(BaseModel):
    source_id: UUID
    company_name: str
    job_title: str
    location: Optional[str] = None
    start_date: date
    end_date: Optional[date] = None
    bullets: list[str] = Field(default_factory=list)


class ResumeProject(BaseModel):
    source_id: UUID
    name: str
    description: str
    role: Optional[str] = None


class ResumeEducation(BaseModel):
    source_id: UUID
    institution: str
    degree: str
    field_of_study: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None


class ResumeCertification(BaseModel):
    source_id: UUID
    name: str
    issuing_organization: str
    issue_date: Optional[date] = None
    expiry_date: Optional[date] = None


class ResumeDocument(BaseModel):
    header: ResumeHeader
    summary: Optional[str] = None
    skills: list[str] = Field(default_factory=list)
    experiences: list[ResumeExperience] = Field(default_factory=list)
    projects: list[ResumeProject] = Field(default_factory=list)
    education: list[ResumeEducation] = Field(default_factory=list)
    certifications: list[ResumeCertification] = Field(default_factory=list)


def format_date(value: date | None) -> str:
    return value.strftime("%b %Y") if value else "Present"
