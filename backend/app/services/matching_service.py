import re
import uuid
from collections import defaultdict
from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.core.errors import NotFoundError, ValidationError
from app.models.career import CareerClaim, ClaimStatus, CandidateSkill
from app.models.job import Job, JobRequirement, RequirementImportance, RequirementType
from app.models.matching import CandidateJobMatch, MatchAnalysisStatus, MatchDetail, MatchType
from app.models.profile import CareerProfile
from app.models.user import User


MATCHING_ALGORITHM_VERSION = "matching-v1"
MATCH_SCORES = {MatchType.STRONG_MATCH: 100.0, MatchType.PARTIAL_MATCH: 50.0, MatchType.GAP: 0.0}
ALLOWED_STATUSES = {ClaimStatus.EVIDENCE_BACKED, ClaimStatus.CANDIDATE_CONFIRMED, ClaimStatus.SELF_DECLARED}
ALIASES = {"postgres": "postgresql", "postgresql db": "postgresql", "restful api": "rest api", "rest apis": "rest api"}


def normalize(value: str | None) -> str:
    cleaned = re.sub(r"[^a-z0-9+#/ ]+", " ", (value or "").lower()).strip()
    cleaned = re.sub(r"\s+", " ", cleaned)
    return ALIASES.get(cleaned, cleaned)


def years_between(start: date | None, end: date | None) -> float | None:
    if not start:
        return None
    finish = end or date.today()
    if finish < start:
        return None
    return round((finish - start).days / 365.25, 2)


class MatchingService:
    @staticmethod
    def _get_job(db: Session, user: User, job_id: uuid.UUID) -> Job:
        job = db.execute(select(Job).where(Job.id == job_id, Job.user_id == user.id)).scalar_one_or_none()
        if not job:
            raise NotFoundError("Job was not found.")
        return job

    @staticmethod
    def run_match(db: Session, user: User, job_id: uuid.UUID) -> CandidateJobMatch:
        job = MatchingService._get_job(db, user, job_id)
        profile = db.execute(select(CareerProfile).where(CareerProfile.user_id == user.id)).scalar_one_or_none()
        if not profile:
            raise NotFoundError("Career profile was not found.")
        requirements = db.execute(select(JobRequirement).where(JobRequirement.job_id == job.id).order_by(JobRequirement.created_at)).scalars().all()
        if not requirements:
            raise ValidationError("Analyze the job description before matching.", {"code": "REQUIREMENTS_NOT_READY"})
        claims = db.execute(select(CareerClaim).where(CareerClaim.career_profile_id == profile.id, CareerClaim.status.in_(ALLOWED_STATUSES))).scalars().all()
        candidate_skills = db.execute(select(CandidateSkill).options(selectinload(CandidateSkill.skill)).where(CandidateSkill.career_profile_id == profile.id)).scalars().all()
        skill_years = {normalize(item.skill.normalized_name): float(item.years_used) for item in candidate_skills if item.years_used is not None}

        result = CandidateJobMatch(
            career_profile_id=profile.id,
            job_id=job.id,
            algorithm_version=MATCHING_ALGORITHM_VERSION,
            overall_score=0,
            profile_coverage=0,
            analysis_status=MatchAnalysisStatus.COMPLETE,
            critical_gaps=[],
        )
        db.add(result)
        db.flush()

        scores: dict[str, list[float]] = defaultdict(list)
        evaluated = 0
        critical_gaps: list[str] = []
        for requirement in requirements:
            requirement_key = normalize(requirement.skill_name or requirement.requirement_text)
            if requirement.requirement_type == RequirementType.EXPERIENCE:
                matching_claims = [
                    claim for claim in claims
                    if normalize(claim.skill_name or claim.subject) in normalize(requirement.requirement_text)
                ]
            else:
                matching_claims = [claim for claim in claims if normalize(claim.skill_name or claim.subject) == requirement_key]
            best_claim = matching_claims[0] if matching_claims else None
            candidate_years = skill_years.get(requirement_key)
            if candidate_years is None and best_claim:
                candidate_years = years_between(best_claim.start_date, best_claim.end_date)
            match_type, score, explanation, gap_category = MatchingService._evaluate(requirement, best_claim, candidate_years)
            if match_type != MatchType.UNKNOWN:
                evaluated += 1
                scores[requirement.importance].append(score)
            if requirement.importance == RequirementImportance.REQUIRED and match_type in {MatchType.GAP, MatchType.PARTIAL_MATCH}:
                critical_gaps.append(explanation)
            db.add(MatchDetail(match_id=result.id, job_requirement_id=requirement.id, career_claim_id=best_claim.id if best_claim else None, match_type=match_type, score=score, explanation=explanation, gap_category=gap_category))

        required_score = sum(scores[RequirementImportance.REQUIRED]) / len(scores[RequirementImportance.REQUIRED]) if scores[RequirementImportance.REQUIRED] else None
        preferred_score = sum(scores[RequirementImportance.PREFERRED]) / len(scores[RequirementImportance.PREFERRED]) if scores[RequirementImportance.PREFERRED] else None
        if required_score is None:
            overall = preferred_score or 0.0
        elif preferred_score is None:
            overall = required_score
        else:
            overall = required_score * 0.70 + preferred_score * 0.30
        result.required_score = required_score
        result.preferred_score = preferred_score
        result.overall_score = round(overall, 2)
        result.profile_coverage = round((evaluated / len(requirements)) * 100, 2)
        result.critical_gaps = critical_gaps
        result.analysis_status = MatchAnalysisStatus.INCOMPLETE if any(detail.match_type == MatchType.UNKNOWN for detail in result.details) else (MatchAnalysisStatus.COMPLETE_WITH_GAPS if critical_gaps else MatchAnalysisStatus.COMPLETE)
        db.flush()
        db.expire(result, ["details"])
        return db.execute(select(CandidateJobMatch).options(selectinload(CandidateJobMatch.details)).where(CandidateJobMatch.id == result.id)).scalar_one()

    @staticmethod
    def _evaluate(requirement: JobRequirement, claim: CareerClaim | None, candidate_years: float | None) -> tuple[MatchType, float, str, str | None]:
        if requirement.requirement_type == RequirementType.CONTEXT:
            return MatchType.UNKNOWN, 0.0, f"{requirement.requirement_text} is contextual and does not establish a candidate qualification.", "context_gap"
        if not claim:
            return MatchType.GAP, 0.0, f"No supported candidate claim was found for {requirement.skill_name or requirement.requirement_text}.", "skill_gap"
        if claim.experience_type != (requirement.experience_type or claim.experience_type):
            return MatchType.PARTIAL_MATCH, 50.0, f"Candidate evidence is {claim.experience_type}, while the requirement asks for {requirement.experience_type} experience.", "experience_type_gap"
        if requirement.minimum_years is not None:
            years = candidate_years or years_between(claim.start_date, claim.end_date) or 0.0
            if years < requirement.minimum_years:
                return MatchType.PARTIAL_MATCH, 50.0, f"Candidate has approximately {years:.2f} years against the requested {requirement.minimum_years}+ years.", "duration_gap"
        if claim.status == ClaimStatus.SELF_DECLARED:
            return MatchType.PARTIAL_MATCH, 50.0, "The candidate has declared this capability, but supporting evidence is limited.", "evidence_gap"
        return MatchType.STRONG_MATCH, 100.0, f"Supported by the candidate claim: {claim.claim_text}", None


matching_service = MatchingService()