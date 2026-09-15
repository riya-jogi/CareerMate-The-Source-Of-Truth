import uuid

from fastapi import APIRouter, status
from sqlalchemy import select

from app.api.deps import CurrentUser, DatabaseSession
from app.models.career import CandidateSkill, Certification, Education, Experience, Project
from app.schemas.profile import (
    CandidateSkillCreate,
    CandidateSkillRead,
    CertificationCreate,
    CertificationRead,
    CareerProfileRead,
    EducationCreate,
    EducationRead,
    ExperienceCreate,
    ExperienceRead,
    ProfileUpdate,
    ProjectCreate,
    ProjectRead,
)
from app.services.profile_service import profile_service

router = APIRouter(prefix="/profile", tags=["Career Profile"])


@router.get("", response_model=CareerProfileRead)
def get_profile(current_user: CurrentUser, db: DatabaseSession):
    return _serialize_profile(profile_service.get_profile(db, current_user))


@router.put("", response_model=CareerProfileRead)
def update_profile(payload: ProfileUpdate, current_user: CurrentUser, db: DatabaseSession):
    return _serialize_profile(profile_service.update_profile(db, current_user, payload))


def _serialize_profile(profile):
    result = CareerProfileRead.model_validate(profile)
    result.skills = [
        CandidateSkillRead(
            id=item.id,
            name=item.skill.name,
            normalized_name=item.skill.normalized_name,
            category=item.skill.category,
            experience_type=item.experience_type,
            proficiency=item.proficiency,
            years_used=float(item.years_used) if item.years_used is not None else None,
            first_used=item.first_used,
            last_used=item.last_used,
            created_at=item.created_at,
            updated_at=item.updated_at,
        )
        for item in profile.candidate_skills
    ]
    return result


@router.post("/experiences", response_model=ExperienceRead, status_code=status.HTTP_201_CREATED)
def create_experience(payload: ExperienceCreate, current_user: CurrentUser, db: DatabaseSession):
    return profile_service.add_item(db, current_user, Experience, payload)


@router.delete("/experiences/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_experience(item_id: uuid.UUID, current_user: CurrentUser, db: DatabaseSession):
    profile_service.delete_item(db, current_user, Experience, item_id)


@router.put("/experiences/{item_id}", response_model=ExperienceRead)
def update_experience(item_id: uuid.UUID, payload: ExperienceCreate, current_user: CurrentUser, db: DatabaseSession):
    return profile_service.update_item(db, current_user, Experience, item_id, payload)


@router.post("/projects", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
def create_project(payload: ProjectCreate, current_user: CurrentUser, db: DatabaseSession):
    return profile_service.add_item(db, current_user, Project, payload)


@router.delete("/projects/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(item_id: uuid.UUID, current_user: CurrentUser, db: DatabaseSession):
    profile_service.delete_item(db, current_user, Project, item_id)


@router.put("/projects/{item_id}", response_model=ProjectRead)
def update_project(item_id: uuid.UUID, payload: ProjectCreate, current_user: CurrentUser, db: DatabaseSession):
    return profile_service.update_item(db, current_user, Project, item_id, payload)


@router.post("/education", response_model=EducationRead, status_code=status.HTTP_201_CREATED)
def create_education(payload: EducationCreate, current_user: CurrentUser, db: DatabaseSession):
    return profile_service.add_item(db, current_user, Education, payload)


@router.delete("/education/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_education(item_id: uuid.UUID, current_user: CurrentUser, db: DatabaseSession):
    profile_service.delete_item(db, current_user, Education, item_id)


@router.put("/education/{item_id}", response_model=EducationRead)
def update_education(item_id: uuid.UUID, payload: EducationCreate, current_user: CurrentUser, db: DatabaseSession):
    return profile_service.update_item(db, current_user, Education, item_id, payload)


@router.post("/certifications", response_model=CertificationRead, status_code=status.HTTP_201_CREATED)
def create_certification(payload: CertificationCreate, current_user: CurrentUser, db: DatabaseSession):
    return profile_service.add_item(db, current_user, Certification, payload)


@router.delete("/certifications/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_certification(item_id: uuid.UUID, current_user: CurrentUser, db: DatabaseSession):
    profile_service.delete_item(db, current_user, Certification, item_id)


@router.put("/certifications/{item_id}", response_model=CertificationRead)
def update_certification(item_id: uuid.UUID, payload: CertificationCreate, current_user: CurrentUser, db: DatabaseSession):
    return profile_service.update_item(db, current_user, Certification, item_id, payload)


@router.post("/skills", response_model=CandidateSkillRead, status_code=status.HTTP_201_CREATED)
def create_skill(payload: CandidateSkillCreate, current_user: CurrentUser, db: DatabaseSession):
    profile_service.add_skill(db, current_user, payload)
    profile = profile_service.get_profile(db, current_user)
    normalized_name = payload.name.strip().lower()
    return next(item for item in _serialize_profile(profile).skills if item.normalized_name == normalized_name)


@router.delete("/skills/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_skill(item_id: uuid.UUID, current_user: CurrentUser, db: DatabaseSession):
    profile_service.delete_item(db, current_user, CandidateSkill, item_id)