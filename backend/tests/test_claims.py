import uuid

from fastapi.testclient import TestClient

from app.main import app


def _authenticated_client(suffix: str = "claims") -> TestClient:
    unique = uuid.uuid4().hex[:8]
    email = f"{suffix}_{unique}@example.com"
    password = "SecurePass@2026!"
    client = TestClient(app)
    registered = client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": password, "full_name": "Claim Candidate"},
    )
    assert registered.status_code == 201
    login = client.post("/api/v1/auth/login", json={"email": email, "password": password})
    assert login.status_code == 200
    client.headers.update({"Authorization": f"Bearer {login.json()['access_token']}"})
    return client


def test_claim_lifecycle_and_status_transitions():
    authenticated = _authenticated_client("claims_lifecycle")

    claim = authenticated.post(
        "/api/v1/claims",
        json={
            "claim_type": "skill",
            "claim_text": "Used FastAPI to build internal APIs.",
            "subject": "FastAPI",
            "context": "Built internal backend services",
            "experience_type": "professional",
            "skill_name": "FastAPI",
        },
    )
    assert claim.status_code == 201
    claim_id = claim.json()["id"]
    assert claim.json()["status"] == "unsupported"

    evidence = authenticated.post(
        f"/api/v1/claims/{claim_id}/evidence",
        json={
            "source_type": "candidate_input",
            "source_reference": "career profile review",
            "content": "Candidate confirmed using FastAPI in the internal services project.",
        },
    )
    assert evidence.status_code == 201

    refreshed = authenticated.get(f"/api/v1/claims/{claim_id}")
    assert refreshed.status_code == 200
    assert refreshed.json()["status"] == "evidence_backed"

    confirmed = authenticated.post(f"/api/v1/claims/{claim_id}/confirm")
    assert confirmed.status_code == 200
    assert confirmed.json()["status"] == "candidate_confirmed"


def test_claims_are_isolated_by_owner():
    owner = _authenticated_client("claims_owner")
    guest = _authenticated_client("claims_guest")

    created = owner.post(
        "/api/v1/claims",
        json={
            "claim_type": "project",
            "claim_text": "Led a data ingestion project.",
            "subject": "Data ingestion",
            "context": "Internal platform",
            "experience_type": "professional",
        },
    )
    assert created.status_code == 201
    claim_id = created.json()["id"]

    response = guest.get(f"/api/v1/claims/{claim_id}")
    assert response.status_code == 404
