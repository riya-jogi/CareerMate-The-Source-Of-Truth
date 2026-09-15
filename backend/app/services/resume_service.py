import hashlib
import re
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.errors import NotFoundError, ValidationError
from app.models.career import CareerClaim, ClaimEvidence, ClaimStatus, ClaimType, Evidence, EvidenceSource
from app.models.profile import CareerProfile
from app.models.resume import ProposalDecision, ProposalType, ResumeFile, ResumeProposal
from app.models.user import User
from app.services.profile_service import profile_service
from app.schemas.resume import ProposalDecision as ProposalDecisionSchema, ResumeUploadCreate
from app.services.resume_parser import parse_resume_bytes


class ResumeService:
    @staticmethod
    def _get_profile_for_user(db: Session, user: User) -> CareerProfile:
        return profile_service.get_profile(db, user)

    @staticmethod
    def list_resumes(db: Session, user: User) -> list[ResumeFile]:
        profile = ResumeService._get_profile_for_user(db, user)
        return db.execute(
            select(ResumeFile)
            .where(ResumeFile.career_profile_id == profile.id)
            .order_by(ResumeFile.created_at.desc())
        ).scalars().all()

    @staticmethod
    def get_resume(db: Session, user: User, resume_id: uuid.UUID) -> ResumeFile:
        profile = ResumeService._get_profile_for_user(db, user)
        resume = db.execute(
            select(ResumeFile).where(ResumeFile.id == resume_id, ResumeFile.career_profile_id == profile.id)
        ).scalar_one_or_none()
        if not resume:
            raise NotFoundError("Resume not found.")
        return resume

    @staticmethod
    def upload_resume(db: Session, user: User, payload: ResumeUploadCreate, raw_bytes: Optional[bytes] = None) -> ResumeFile:
        profile = ResumeService._get_profile_for_user(db, user)
        if raw_bytes is None:
            raw_bytes = payload.content.encode("utf-8")
        if len(raw_bytes) > settings.MAX_RESUME_FILE_SIZE:
            raise ValidationError("Resume file exceeds the configured 10 MB limit.", {"code": "FILE_TOO_LARGE"})
        filename = payload.filename.strip()
        parsed_text = parse_resume_bytes(filename, payload.content_type, raw_bytes)
        if not parsed_text:
            raise ValidationError("The resume contains no extractable text.", {"code": "FILE_NO_TEXT"})

        storage_root = Path(settings.STORAGE_PATH).resolve()
        storage_key = f"resumes/{profile.id}/{uuid.uuid4()}_{Path(filename).name}"
        storage_path = storage_root / storage_key
        storage_path.parent.mkdir(parents=True, exist_ok=True)
        storage_path.write_bytes(raw_bytes)
        resume = ResumeFile(
            career_profile_id=profile.id,
            filename=filename,
            content_type=payload.content_type.strip(),
            content=parsed_text,
            storage_key=storage_key,
            checksum=hashlib.sha256(raw_bytes).hexdigest(),
            file_size=len(raw_bytes),
            status="uploaded",
        )
        db.add(resume)
        db.flush()
        return resume

    @staticmethod
    def extract_resume(db: Session, user: User, resume_id: uuid.UUID) -> list[ResumeProposal]:
        resume = ResumeService.get_resume(db, user, resume_id)
        text = resume.content or ""

        proposals: list[ResumeProposal] = []
        for skill_name in ["Python", "FastAPI", "PostgreSQL", "Docker", "SQLAlchemy", "React", "TypeScript", "JavaScript"]:
            if re.search(rf"\b{re.escape(skill_name)}\b", text, flags=re.IGNORECASE):
                proposals.append(
                    ResumeProposal(
                        resume_file_id=resume.id,
                        proposal_type=ProposalType.SKILL,
                        field_name="skills",
                        proposed_value=skill_name,
                        source_excerpt=skill_name,
                        confidence=0.9,
                        decision=ProposalDecision.PENDING,
                    )
                )

        if re.search(r"\b(?:senior|lead|principal)\b.*\b(?:engineer|developer)\b", text, flags=re.IGNORECASE):
            match = re.search(r"(?:senior|lead|principal)\s+[A-Za-z0-9+\-./ ]*(?:engineer|developer)", text, flags=re.IGNORECASE)
            proposed_value = (match.group(0).strip() if match else "Senior software engineer").title()
            proposals.append(
                ResumeProposal(
                    resume_file_id=resume.id,
                    proposal_type=ProposalType.EXPERIENCE,
                    field_name="title",
                    proposed_value=proposed_value,
                    source_excerpt=text[:200],
                    confidence=0.82,
                    decision=ProposalDecision.PENDING,
                )
            )

        if not proposals:
            proposals.append(
                ResumeProposal(
                    resume_file_id=resume.id,
                    proposal_type=ProposalType.SUMMARY,
                    field_name="summary",
                    proposed_value=text[:180],
                    source_excerpt=text[:200],
                    confidence=0.5,
                    decision=ProposalDecision.PENDING,
                )
            )

        resume.status = "extracted"
        resume.extracted_at = datetime.now(timezone.utc)
        db.add_all(proposals)
        db.flush()
        return proposals

    @staticmethod
    def review_proposal(db: Session, user: User, proposal_id: uuid.UUID, review) -> ResumeProposal:
        proposal = db.execute(
            select(ResumeProposal)
            .join(ResumeFile, ResumeFile.id == ResumeProposal.resume_file_id)
            .where(ResumeProposal.id == proposal_id, ResumeFile.career_profile_id == profile_service.get_profile(db, user).id)
        ).scalar_one_or_none()
        if not proposal:
            raise NotFoundError("Proposal not found.")
        if review.proposed_value:
            proposal.proposed_value = review.proposed_value
        proposal.decision = review.decision
        proposal.review_notes = review.notes
        if review.decision in {ProposalDecisionSchema.ACCEPTED, ProposalDecisionSchema.EDITED}:
            ResumeService._apply_accepted_proposal(db, user, proposal)
        db.flush()
        return proposal

    @staticmethod
    def _apply_accepted_proposal(db: Session, user: User, proposal: ResumeProposal) -> None:
        profile = ResumeService._get_profile_for_user(db, user)
        resume = proposal.resume_file
        if proposal.proposal_type == ProposalType.SUMMARY:
            profile.summary = proposal.proposed_value
            return
        if proposal.proposal_type != ProposalType.SKILL:
            return

        from app.schemas.profile import CandidateSkillCreate
        from app.models.career import ExperienceType

        normalized = proposal.proposed_value.strip().lower()
        existing = next((item for item in profile.candidate_skills if item.skill.normalized_name == normalized), None)
        if not existing:
            profile_service.add_skill(
                db,
                user,
                CandidateSkillCreate(name=proposal.proposed_value, experience_type=ExperienceType.PROFESSIONAL),
            )
        excerpt = proposal.source_excerpt or proposal.proposed_value
        evidence = Evidence(
            career_profile_id=profile.id,
            source_type=EvidenceSource.RESUME,
            source_reference=resume.filename,
            content=excerpt,
            content_hash=hashlib.sha256(excerpt.encode("utf-8")).hexdigest(),
        )
        claim = CareerClaim(
            career_profile_id=profile.id,
            claim_type=ClaimType.SKILL,
            claim_text=f"Uses {proposal.proposed_value}.",
            subject=proposal.proposed_value,
            skill_name=proposal.proposed_value,
            status=ClaimStatus.EVIDENCE_BACKED,
            confidence=float(proposal.confidence),
        )
        db.add_all([evidence, claim])
        db.flush()
        db.add(ClaimEvidence(claim_id=claim.id, evidence_id=evidence.id))


resume_service = ResumeService()
