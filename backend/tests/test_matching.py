import uuid

from fastapi.testclient import TestClient

from app.main import app


def _authenticated_client() -> TestClient:
    client = TestClient(app)
    email = f"match_{uuid.uuid4().hex[:8]}@example.com"
    password = "SecurePass@2026!"
    assert client.post("/api/v1/auth/register", json={"email": email, "password": password, "full_name": "Match Candidate"}).status_code == 201
    login = client.post("/api/v1/auth/login", json={"email": email, "password": password})
    assert login.status_code == 200
    client.headers.update({"Authorization": f"Bearer {login.json()['access_token']}"})
    return client


def _claim_with_evidence(client: TestClient, subject: str, claim_text: str, start_date: str | None = None, experience_type: str = "professional") -> None:
    payload = {"claim_type": "skill", "claim_text": claim_text, "subject": subject, "skill_name": subject, "experience_type": experience_type}
    if start_date:
        payload["start_date"] = start_date
    created = client.post("/api/v1/claims", json=payload)
    assert created.status_code == 201
    claim_id = created.json()["id"]
    evidence = client.post(f"/api/v1/claims/{claim_id}/evidence", json={"source_type": "candidate_input", "source_reference": "match test", "content": claim_text})
    assert evidence.status_code == 201


def test_matching_scores_requirements_and_surfaces_critical_gaps():
    client = _authenticated_client()
    _claim_with_evidence(client, "Python", "Developed backend APIs using Python.", "2024-01-01")
    _claim_with_evidence(client, "FastAPI", "Developed APIs using FastAPI.", "2024-01-01")
    _claim_with_evidence(client, "Docker", "Used Docker in a personal project.", experience_type="personal")

    created = client.post(
        "/api/v1/jobs",
        json={"title": "Backend Developer", "description": "Python and FastAPI required. Docker preferred. 3+ years experience."},
    )
    assert created.status_code == 201
    job_id = created.json()["id"]
    assert client.post(f"/api/v1/jobs/{job_id}/analyze").status_code == 200

    matched = client.post(f"/api/v1/jobs/{job_id}/match")
    assert matched.status_code == 200
    body = matched.json()
    assert body["algorithm_version"] == "matching-v1"
    assert 0 <= body["overall_score"] <= 100
    assert 0 < body["profile_coverage"] <= 100
    assert body["analysis_status"] == "complete_with_gaps"
    assert any("years" in gap for gap in body["critical_gaps"])
    assert any(detail["match_type"] == "strong_match" for detail in body["details"])
    assert any(detail["match_type"] == "partial_match" for detail in body["details"])


def test_matching_isolated_by_owner():
    owner = _authenticated_client()
    guest = _authenticated_client()
    created = owner.post("/api/v1/jobs", json={"description": "A backend job requiring Python and APIs."})
    assert created.status_code == 201
    response = guest.post(f"/api/v1/jobs/{created.json()['id']}/match")
    assert response.status_code == 404
