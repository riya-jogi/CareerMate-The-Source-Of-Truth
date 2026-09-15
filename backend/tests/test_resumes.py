import uuid

from fastapi.testclient import TestClient

from app.main import app


def _authenticated_client(suffix: str = "resume") -> TestClient:
    unique = uuid.uuid4().hex[:8]
    email = f"{suffix}_{unique}@example.com"
    password = "SecurePass@2026!"
    client = TestClient(app)
    registered = client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": password, "full_name": "Resume Candidate"},
    )
    assert registered.status_code == 201
    login = client.post("/api/v1/auth/login", json={"email": email, "password": password})
    assert login.status_code == 200
    client.headers.update({"Authorization": f"Bearer {login.json()['access_token']}"})
    return client


def test_resume_upload_and_extraction_review():
    authenticated = _authenticated_client("resume_upload")

    uploaded = authenticated.post(
        "/api/v1/resumes/upload",
        json={
            "filename": "candidate_resume.txt",
            "content_type": "text/plain",
            "content": "Senior Python engineer with FastAPI, PostgreSQL, and Docker. Built backend APIs.",
        },
    )
    assert uploaded.status_code == 201
    resume_id = uploaded.json()["id"]

    list_response = authenticated.get("/api/v1/resumes")
    assert list_response.status_code == 200
    assert len(list_response.json()) >= 1

    extracted = authenticated.post(f"/api/v1/resumes/{resume_id}/extract")
    assert extracted.status_code == 201
    proposals = extracted.json()["proposals"]
    assert len(proposals) >= 2
    assert any(item["proposal_type"] == "skill" and item["proposed_value"] == "Python" for item in proposals)

    proposal_id = proposals[0]["id"]
    reviewed = authenticated.patch(
        f"/api/v1/resumes/proposals/{proposal_id}/review",
        json={"decision": "accepted"},
    )
    assert reviewed.status_code == 200
    assert reviewed.json()["decision"] == "accepted"


def test_resume_access_is_isolated_by_owner():
    owner = _authenticated_client("resume_owner")
    guest = _authenticated_client("resume_guest")

    uploaded = owner.post(
        "/api/v1/resumes/upload",
        json={
            "filename": "owner_resume.txt",
            "content_type": "text/plain",
            "content": "Python backend engineer with FastAPI.",
        },
    )
    assert uploaded.status_code == 201
    resume_id = uploaded.json()["id"]

    response = guest.get(f"/api/v1/resumes/{resume_id}")
    assert response.status_code == 404
