import hashlib
import uuid
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.errors import ConflictError, NotFoundError
from app.models.career import CareerClaim, ClaimEvidence, ClaimStatus, Evidence, EvidenceSource
from app.models.profile import CareerProfile
from app.models.user import User


class ClaimService:
    @staticmethod
    def get_profile_claims(db: Session, user: User):
        profile = db.execute(select(CareerProfile).where(CareerProfile.user_id == user.id)).scalar_one_or_none()
        if not profile:
            raise NotFoundError("Career profile was not found.")
        return profile

    @staticmethod
    def _get_claim_for_user(db: Session, user: User, claim_id: uuid.UUID) -> CareerClaim:
        profile = ClaimService.get_profile_claims(db, user)
        claim = db.execute(
            select(CareerClaim).where(CareerClaim.id == claim_id, CareerClaim.career_profile_id == profile.id)
        ).scalar_one_or_none()
        if not claim:
            raise NotFoundError("Claim not found.")
        return claim

    @staticmethod
    def create_claim(db: Session, user: User, payload) -> CareerClaim:
        profile = ClaimService.get_profile_claims(db, user)
        claim = CareerClaim(
            career_profile_id=profile.id,
            claim_type=payload.claim_type,
            claim_text=payload.claim_text,
            subject=payload.subject,
            context=payload.context,
            experience_type=payload.experience_type,
            start_date=payload.start_date,
            end_date=payload.end_date,
            proficiency=payload.proficiency,
            skill_name=payload.skill_name,
            status=ClaimStatus.UNSUPPORTED,
            confidence=0.0,
        )
        db.add(claim)
        db.flush()
        return claim

    @staticmethod
    def add_evidence(db: Session, user: User, claim_id: uuid.UUID, payload) -> Evidence:
        claim = ClaimService._get_claim_for_user(db, user, claim_id)
        profile = ClaimService.get_profile_claims(db, user)
        content_hash = hashlib.sha256(payload.content.encode("utf-8")).hexdigest()
        evidence = Evidence(
            career_profile_id=profile.id,
            source_type=payload.source_type,
            source_reference=payload.source_reference,
            content=payload.content,
            content_hash=content_hash,
        )
        db.add(evidence)
        db.flush()

        link = ClaimEvidence(claim_id=claim.id, evidence_id=evidence.id)
        db.add(link)
        db.flush()

        if claim.status == ClaimStatus.UNSUPPORTED:
            claim.status = ClaimStatus.EVIDENCE_BACKED
            claim.confidence = 0.75

        return evidence

    @staticmethod
    def confirm_claim(db: Session, user: User, claim_id: uuid.UUID) -> CareerClaim:
        claim = ClaimService._get_claim_for_user(db, user, claim_id)
        if claim.status == ClaimStatus.UNSUPPORTED:
            raise ConflictError("Claim cannot be confirmed without evidence.")
        claim.status = ClaimStatus.CANDIDATE_CONFIRMED
        claim.confidence = 1.0
        claim.candidate_confirmed_at = __import__("datetime").datetime.now(__import__("datetime").timezone.utc)
        db.flush()
        return claim

    @staticmethod
    def get_claim(db: Session, user: User, claim_id: uuid.UUID) -> CareerClaim:
        return ClaimService._get_claim_for_user(db, user, claim_id)


claim_service = ClaimService()
