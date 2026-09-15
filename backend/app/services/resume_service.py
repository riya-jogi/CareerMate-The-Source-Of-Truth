import re
import uuid
from datetime import datetime, timezone
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.errors import NotFoundError
from app.models.profile import CareerProfile
from app.models.resume import ProposalDecision, ProposalType, ResumeFile, ResumeProposal
from app.models.user import User
from app.services.profile_service import profile_service
from app.schemas.resume import ProposalDecision as ProposalDecisionSchema, ResumeUploadCreate


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
    def upload_resume(db: Session, user: User, payload: ResumeUploadCreate) -> ResumeFile:
        profile = ResumeService._get_profile_for_user(db, user)
        resume = ResumeFile(
            career_profile_id=profile.id,
            filename=payload.filename.strip(),
            content_type=payload.content_type.strip(),
            content=payload.content,
            file_size=len(payload.content.encode("utf-8")),
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
    def review_proposal(db: Session, user: User, proposal_id: uuid.UUID, decision: ProposalDecisionSchema, notes: str | None = None):
        proposal = db.execute(
            select(ResumeProposal)
            .join(ResumeFile, ResumeFile.id == ResumeProposal.resume_file_id)
            .where(ResumeProposal.id == proposal_id, ResumeFile.career_profile_id == profile_service.get_profile(db, user).id)
        ).scalar_one_or_none()
        if not proposal:
            raise NotFoundError("Proposal not found.")
        proposal.decision = decision
        proposal.review_notes = notes
        db.flush()
        return proposal


resume_service = ResumeService()
