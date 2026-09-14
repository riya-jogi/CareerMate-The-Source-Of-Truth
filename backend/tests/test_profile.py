import uuid

from fastapi.testclient import TestClient


def _authenticated_client(client: TestClient) -> TestClient:
    suffix = uuid.uuid4().hex[:8]
    email = f"profile_{suffix}@example.com"
    password = "SecurePass@2026!"
    registered = client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": password, "full_name": "Profile Candidate"},
    )
    assert registered.status_code == 201
    login = client.post("/api/v1/auth/login", json={"email": email, "password": password})
    assert login.status_code == 200
    client.headers.update({"Authorization": f"Bearer {login.json()['access_token']}"})
    return client


def test_profile_update_and_structured_career_data(client: TestClient):
    authenticated = _authenticated_client(client)

    update = authenticated.put(
        "/api/v1/profile",
        json={
            "headline": "Python Backend Developer",
            "summary": "Builds reliable backend systems.",
            "location": "Remote",
        },
    )
    assert update.status_code == 200
    assert update.json()["headline"] == "Python Backend Developer"

    experience = authenticated.post(
        "/api/v1/profile/experiences",
        json={
            "company_name": "Example Labs",
            "job_title": "Backend Engineer",
            "start_date": "2024-01-01",
            "is_current": True,
            "description": "Built REST APIs.",
        },
    )
    assert experience.status_code == 201
    experience_id = experience.json()["id"]

    skill = authenticated.post("/api/v1/profile/skills", json={"name": " FastAPI "})
    assert skill.status_code == 201
    assert skill.json()["normalized_name"] == "fastapi"

    profile = authenticated.get("/api/v1/profile")
    assert profile.status_code == 200
    assert len(profile.json()["experiences"]) == 1
    assert profile.json()["skills"][0]["name"] == "FastAPI"

    deleted = authenticated.delete(f"/api/v1/profile/experiences/{experience_id}")
    assert deleted.status_code == 204


def test_profile_rejects_invalid_date_ranges(client: TestClient):
    authenticated = _authenticated_client(client)
    response = authenticated.post(
        "/api/v1/profile/experiences",
        json={
            "company_name": "Example Labs",
            "job_title": "Backend Engineer",
            "start_date": "2025-01-01",
            "end_date": "2024-01-01",
        },
    )
    assert response.status_code == 422
