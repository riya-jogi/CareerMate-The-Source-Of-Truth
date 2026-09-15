import logging
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.career import CareerClaim, Evidence
from app.models.job import Job, JobAnalysisStatus
from app.models.matching import CandidateJobMatch
from app.models.resume_version import Resume, ResumeVersion, ResumeVersionStatus
from app.models.user import User
from app.schemas.dashboard import DashboardSummaryResponse

logger = logging.getLogger("careermate.dashboard")


class DashboardService:
    """Service to aggregate dashboard metrics and profile progress for candidates."""

    @staticmethod
    def calculate_profile_completeness(user: User) -> int:
        """
        Calculates profile completeness percentage based on the candidate's
        established CareerProfile and account information.
        """
        score = 0

        # Base active account & verified identity: 20%
        if user.is_active:
            score += 20

        # Full name provided: 10%
        if user.full_name and len(user.full_name.strip()) >= 2:
            score += 10

        profile = user.career_profile
        if profile:
            # Professional headline: 20%
            if profile.headline and len(profile.headline.strip()) > 0:
                score += 20

            # Career summary: 20%
            if profile.summary and len(profile.summary.strip()) > 0:
                score += 20

            # Contact / Location: 15%
            if (profile.location and len(profile.location.strip()) > 0) or (
                profile.phone and len(profile.phone.strip()) > 0
            ):
                score += 15

            # Professional links (LinkedIn / GitHub / Portfolio): 15%
            if (
                profile.linkedin_url
                or profile.github_url
                or profile.portfolio_url
            ):
                score += 15

        return min(score, 100)

    def get_dashboard_summary(self, db: Session, user: User) -> DashboardSummaryResponse:
        """
        Aggregates summary statistics for the authenticated candidate.
        Currently queries the user's profile and initial anchors.
        As modules 2-6 are implemented, this will dynamically count
        CareerClaims, Evidence, Resumes, and Jobs from their respective tables.
        """
        profile = user.career_profile
        completeness = self.calculate_profile_completeness(user)

        headline = profile.headline if profile else None

        career_claims_count = db.scalar(select(func.count(CareerClaim.id)).where(CareerClaim.career_profile_id == profile.id)) if profile else 0
        evidence_sources_count = db.scalar(select(func.count(Evidence.id)).where(Evidence.career_profile_id == profile.id)) if profile else 0
        analyzed_jobs_count = db.scalar(select(func.count(Job.id)).where(Job.user_id == user.id, Job.analysis_status == JobAnalysisStatus.COMPLETED)) or 0
        optimized_resumes_count = db.scalar(
            select(func.count(ResumeVersion.id))
            .join(Resume, Resume.id == ResumeVersion.resume_id)
            .where(Resume.career_profile_id == profile.id, ResumeVersion.status == ResumeVersionStatus.READY)
        ) if profile else 0
        optimized_resumes_count = optimized_resumes_count or 0
        target_matches_count = db.scalar(
            select(func.count(CandidateJobMatch.id)).where(CandidateJobMatch.career_profile_id == profile.id)
        ) if profile else 0

        return DashboardSummaryResponse(
            candidate_name=user.full_name,
            candidate_email=user.email,
            candidate_headline=headline,
            profile_completeness_percentage=completeness,
            career_claims_count=career_claims_count,
            evidence_sources_count=evidence_sources_count,
            analyzed_jobs_count=analyzed_jobs_count,
            optimized_resumes_count=optimized_resumes_count,
            target_matches_count=target_matches_count,
            active_anchor=profile is not None,
            account_created_at=user.created_at,
            last_login_at=user.last_login_at,
        )


dashboard_service = DashboardService()
