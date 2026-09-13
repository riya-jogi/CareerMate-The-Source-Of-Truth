import uuid
import pytest
from app.core.security import verify_password
from app.models.user import User
from app.models.profile import CareerProfile


def test_register_user_success(client, db_session):
    unique_suffix = uuid.uuid4().hex[:8]
    payload = {
        "email": f"candidate_{unique_suffix}@example.com",
        "password": "SecurePassword123!",
        "full_name": "Jane Doe",
        "headline": "Lead AI Engineer",
    }

    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 201

    data = response.json()
    assert "id" in data
    assert data["email"] == payload["email"].lower()
    assert data["full_name"] == "Jane Doe"
    assert data["is_active"] is True
    assert data["is_verified"] is False
    assert "created_at" in data

    # Security check: Password must NEVER be returned
    assert "password" not in data
    assert "hashed_password" not in data

    # Career profile must be automatically provisioned
    assert "career_profile" in data
    assert data["career_profile"] is not None
    assert data["career_profile"]["headline"] == "Lead AI Engineer"

    # Verify directly in the database
    db_user = db_session.query(User).filter(User.email == payload["email"]).first()
    assert db_user is not None
    assert verify_password("SecurePassword123!", db_user.hashed_password) is True
    assert db_user.career_profile is not None
    assert db_user.career_profile.headline == "Lead AI Engineer"


def test_register_user_email_normalization(client, db_session):
    unique_suffix = uuid.uuid4().hex[:8]
    mixed_email = f"  Candidate.{unique_suffix}@EXAMPLE.Com  "
    expected_email = f"candidate.{unique_suffix}@example.com"

    payload = {
        "email": mixed_email,
        "password": "ValidPassword123@",
        "full_name": "  Normalized Name  ",
        "headline": "Software Architect",
    }

    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == expected_email
    assert data["full_name"] == "Normalized Name"


def test_register_user_duplicate_email_conflict(client):
    unique_suffix = uuid.uuid4().hex[:8]
    email = f"duplicate_{unique_suffix}@example.com"
    payload = {
        "email": email,
        "password": "ValidPassword123@",
        "full_name": "Original Candidate",
    }

    # First registration
    resp1 = client.post("/api/v1/auth/register", json=payload)
    assert resp1.status_code == 201

    # Second registration with same email (even with case difference)
    payload_duplicate = {
        "email": email.upper(),
        "password": "DifferentPassword123@",
        "full_name": "Second Candidate",
    }
    resp2 = client.post("/api/v1/auth/register", json=payload_duplicate)
    assert resp2.status_code == 409
    data = resp2.json()
    assert "error" in data
    assert data["error"]["code"] == "RESOURCE_CONFLICT"
    assert "already exists" in data["error"]["message"].lower()
    assert data["error"]["details"]["field"] == "email"


@pytest.mark.parametrize(
    "weak_password,expected_error_snippet",
    [
        ("short1!", "at least 8 characters"),
        ("nouppercase123!", "uppercase letter"),
        ("NOLOWERCASE123!", "lowercase letter"),
        ("NoNumbersHere!", "digit"),
        ("NoSpecialSymbols123", "special character"),
    ],
)
def test_register_user_password_strength_validation(client, weak_password, expected_error_snippet):
    payload = {
        "email": f"test_{uuid.uuid4().hex[:6]}@example.com",
        "password": weak_password,
        "full_name": "Test Candidate",
    }

    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 422
    data = response.json()
    assert "error" in data
    assert data["error"]["code"] == "REQUEST_VALIDATION_ERROR"
    errors_str = str(data["error"]["details"]["validation_errors"]).lower()
    assert expected_error_snippet.lower() in errors_str


def test_register_user_invalid_full_name(client):
    payload = {
        "email": f"test_{uuid.uuid4().hex[:6]}@example.com",
        "password": "ValidPassword123@",
        "full_name": "   ",
    }

    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 422
    data = response.json()
    assert data["error"]["code"] == "REQUEST_VALIDATION_ERROR"
