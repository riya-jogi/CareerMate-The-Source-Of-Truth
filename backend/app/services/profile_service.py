import re
import uuid
from typing import Type

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.core.errors import ConflictError, NotFoundError
from app.models.career import CandidateSkill, Certification, Education, Experience, Project, Skill
from app.models.profile import CareerProfile
from app.models.user import User
from app.schemas.profile import (
    CandidateSkillCreate,
    CertificationCreate,
    EducationCreate,
    ExperienceCreate,
    ProfileUpdate,
    ProjectCreate,
)


def _normalize_skill(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip()).lower()


class ProfileService:
    @staticmethod
    def get_profile(db: Session, user: User) -> CareerProfile:
        profile = db.execute(
            select(CareerProfile)
            .options(
                joinedload(CareerProfile.experiences),
                joinedload(CareerProfile.projects),
                joinedload(CareerProfile.education),
                joinedload(CareerProfile.certifications),
                joinedload(CareerProfile.candidate_skills).joinedload(CandidateSkill.skill),
            )
            .where(CareerProfile.user_id == user.id)
        ).unique().scalar_one_or_none()
        if not profile:
            raise NotFoundError("Career profile was not found.")
        return profile

    @staticmethod
    def update_profile(db: Session, user: User, payload: ProfileUpdate) -> CareerProfile:
        profile = ProfileService.get_profile(db, user)
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(profile, field, value)
        db.flush()
        return profile

    @staticmethod
    def add_item(db: Session, user: User, model: Type, payload: object):
        profile = ProfileService.get_profile(db, user)
        item = model(career_profile_id=profile.id, **payload.model_dump())
        db.add(item)
        db.flush()
        return item

    @staticmethod
    def add_skill(db: Session, user: User, payload: CandidateSkillCreate) -> CandidateSkill:
        profile = ProfileService.get_profile(db, user)
        normalized_name = _normalize_skill(payload.name)
        skill = db.execute(select(Skill).where(Skill.normalized_name == normalized_name)).scalar_one_or_none()
        if not skill:
            skill = Skill(name=payload.name.strip(), normalized_name=normalized_name, category=payload.category)
            db.add(skill)
            db.flush()

        existing = db.execute(
            select(CandidateSkill).where(
                CandidateSkill.career_profile_id == profile.id,
                CandidateSkill.skill_id == skill.id,
            )
        ).scalar_one_or_none()
        if existing:
            raise ConflictError("This skill is already present in the career profile.", {"skill": skill.name})

        candidate_skill = CandidateSkill(
            career_profile_id=profile.id,
            skill_id=skill.id,
            experience_type=payload.experience_type,
            proficiency=payload.proficiency,
            years_used=payload.years_used,
            first_used=payload.first_used,
            last_used=payload.last_used,
            skill=skill,
        )
        db.add(candidate_skill)
        db.flush()
        return candidate_skill

    @staticmethod
    def delete_item(db: Session, user: User, model: Type, item_id: uuid.UUID) -> None:
        profile = ProfileService.get_profile(db, user)
        item = db.execute(
            select(model).where(model.id == item_id, model.career_profile_id == profile.id)
        ).scalar_one_or_none()
        if not item:
            raise NotFoundError("Career profile item was not found.")
        db.delete(item)
        db.flush()

    @staticmethod
    def update_item(db: Session, user: User, model: Type, item_id: uuid.UUID, payload: object):
        profile = ProfileService.get_profile(db, user)
        item = db.execute(
            select(model).where(model.id == item_id, model.career_profile_id == profile.id)
        ).scalar_one_or_none()
        if not item:
            raise NotFoundError("Career profile item was not found.")
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(item, field, value)
        db.flush()
        return item


profile_service = ProfileService()

CAREER_MODELS = {
    "experiences": Experience,
    "projects": Project,
    "education": Education,
    "certifications": Certification,
}