import uuid

from fastapi.testclient import TestClient

from app.main import app


def _authenticated_client() -> TestClient:
    client = TestClient(app)
    email = f"job_{uuid.uuid4().hex[:8]}@example.com"
    password = "SecurePass@2026!"
    registered = client.post("/api/v1/auth/register", json={"email": email, "password": password, "full_name": "Job Candidate"})
    assert registered.status_code == 201
    login = client.post("/api/v1/auth/login", json={"email": email, "password": password})
    assert login.status_code == 200
    client.headers.update({"Authorization": f"Bearer {login.json()['access_token']}"})
    return client


def test_job_analysis_extracts_owned_requirements():
    client = _authenticated_client()
    created = client.post(
        "/api/v1/jobs",
        json={
            "title": "Python Backend Developer",
            "company_name": "Example Labs",
            "description": "Python and FastAPI required. PostgreSQL required. Docker preferred. 3+ years experience.",
        },
    )
    assert created.status_code == 201
    job_id = created.json()["id"]

    analyzed = client.post(f"/api/v1/jobs/{job_id}/analyze")
    assert analyzed.status_code == 200
    assert analyzed.json()["job"]["analysis_status"] == "completed"
    requirements = analyzed.json()["requirements"]
    assert any(item["skill_name"] == "Python" and item["importance"] == "required" for item in requirements)
    assert any(item["skill_name"] == "Docker" and item["importance"] == "preferred" for item in requirements)
    assert any(item["minimum_years"] == 3 for item in requirements)


def test_jobs_are_isolated_by_owner():
    owner = _authenticated_client()
    guest = _authenticated_client()
    created = owner.post("/api/v1/jobs", json={"description": "A backend role requiring Python and APIs."})
    assert created.status_code == 201
    response = guest.get(f"/api/v1/jobs/{created.json()['id']}")
    assert response.status_code == 404
