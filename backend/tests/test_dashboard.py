import uuid
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.security import create_access_token
from app.models.user import User
from app.models.profile import CareerProfile


def test_dashboard_summary_requires_authentication(client: TestClient):
    """Accessing dashboard summary without token should return 401."""
    response = client.get("/api/v1/dashboard/summary")
    assert response.status_code == 401
    data = response.json()
    assert data["error"]["code"] == "AUTHENTICATION_ERROR"


def test_dashboard_summary_returns_candidate_metrics(
    client: TestClient,
    db_session: Session,
):
    """Authenticated candidate receives dynamic dashboard metrics and profile progress."""
    unique_email = f"dashboard_{uuid.uuid4().hex[:8]}@example.com"
    user = User(
        email=unique_email,
        hashed_password="dummy_hashed_password",
        full_name="Morgan Vance",
        is_active=True,
        is_verified=True,
    )
    db_session.add(user)
    db_session.flush()

    profile = CareerProfile(
        user_id=user.id,
        headline="Senior Distributed Systems Engineer",
        summary="Experienced backend platform engineer with a focus on truth-verified architectures.",
        location="San Francisco, CA",
        linkedin_url="https://linkedin.com/in/morganvance",
    )
    db_session.add(profile)
    db_session.commit()
    db_session.refresh(user)

    token = create_access_token(subject=str(user.id))

    response = client.get(
        "/api/v1/dashboard/summary",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    data = response.json()

    assert data["candidate_name"] == "Morgan Vance"
    assert data["candidate_email"] == unique_email
    assert data["candidate_headline"] == "Senior Distributed Systems Engineer"
    assert data["active_anchor"] is True
    # Profile completeness: active (20) + name (10) + headline (20) + summary (20) + location (15) + linkedin (15) = 100
    assert data["profile_completeness_percentage"] == 100
    assert data["career_claims_count"] == 0
    assert data["evidence_sources_count"] == 0
    assert data["analyzed_jobs_count"] == 0
    assert data["optimized_resumes_count"] == 0
    assert data["target_matches_count"] == 0


def test_dashboard_summary_partial_profile_completeness(
    client: TestClient,
    db_session: Session,
):
    """Candidates with only basic fields receive an accurate, partial completeness score."""
    partial_email = f"partial_{uuid.uuid4().hex[:8]}@example.com"
    user = User(
        email=partial_email,
        hashed_password="dummy_hashed_password",
        full_name="Jordan Reed",
        is_active=True,
        is_verified=False,
    )
    db_session.add(user)
    db_session.flush()

    profile = CareerProfile(
        user_id=user.id,
        headline=None,
        summary=None,
    )
    db_session.add(profile)
    db_session.commit()
    db_session.refresh(user)

    token = create_access_token(subject=str(user.id))

    response = client.get(
        "/api/v1/dashboard/summary",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["candidate_name"] == "Jordan Reed"
    assert data["candidate_headline"] is None
    # active (20) + name (10) = 30%
    assert data["profile_completeness_percentage"] == 30
