from datetime import timedelta
import uuid
import pytest

from app.core.security import create_access_token
from app.models.user import User


@pytest.fixture
def active_user(client, db_session):
    """Registers a fresh user and returns user entity and access token."""
    email = f"me_test_{uuid.uuid4().hex[:8]}@example.com"
    password = "ValidPassword@2026!"
    reg_resp = client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": password, "full_name": "Active Candidate", "headline": "Staff AI Engineer"},
    )
    assert reg_resp.status_code == 201
    user_id = reg_resp.json()["id"]

    # Log in to get token
    login_resp = client.post("/api/v1/auth/login", json={"email": email, "password": password})
    assert login_resp.status_code == 200
    token = login_resp.json()["access_token"]

    return {
        "user_id": user_id,
        "email": email,
        "token": token,
    }


def test_get_me_valid_authentication(client, active_user):
    """1. Valid authentication returns user details without sensitive fields."""
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {active_user['token']}"},
    )
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == active_user["user_id"]
    assert data["email"] == active_user["email"].lower()
    assert data["full_name"] == "Active Candidate"
    assert data["is_active"] is True
    assert data["is_verified"] is False
    assert data["career_profile"]["headline"] == "Staff AI Engineer"

    # Security check: No password or secrets returned
    assert "password" not in data
    assert "hashed_password" not in data
    assert "token" not in data


def test_get_me_missing_authentication(client):
    """2. Missing authentication returns 401 Unauthorized."""
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401

    data = response.json()
    assert data["error"]["code"] == "AUTHENTICATION_ERROR"
    assert "not provided" in data["error"]["message"].lower()


def test_get_me_invalid_token(client):
    """3. Invalid token returns 401 Unauthorized."""
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": "Bearer malformed.invalid.jwt_token"},
    )
    assert response.status_code == 401

    data = response.json()
    assert data["error"]["code"] == "AUTHENTICATION_ERROR"
    assert "invalid or expired" in data["error"]["message"].lower()


def test_get_me_wrong_token_type(client, active_user):
    """3b. Token with non-access type returns 401 Unauthorized."""
    # Create token with type='refresh'
    wrong_type_token = create_access_token(
        subject=active_user["user_id"],
        claims={"type": "refresh"},
    )
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {wrong_type_token}"},
    )
    assert response.status_code == 401
    data = response.json()
    assert data["error"]["code"] == "AUTHENTICATION_ERROR"
    assert "access token expected" in data["error"]["message"].lower()


def test_get_me_expired_token(client, active_user):
    """4. Expired access token returns 401 Unauthorized."""
    expired_token = create_access_token(
        subject=active_user["user_id"],
        expires_delta=timedelta(seconds=-10),  # Expired in past
    )
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {expired_token}"},
    )
    assert response.status_code == 401

    data = response.json()
    assert data["error"]["code"] == "AUTHENTICATION_ERROR"
    assert "expired" in data["error"]["message"].lower()


def test_get_me_inactive_user(client, active_user, db_session):
    """5. Deactivated user returns 403 Forbidden."""
    user = db_session.get(User, uuid.UUID(active_user["user_id"]))
    user.is_active = False
    db_session.commit()

    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {active_user['token']}"},
    )
    assert response.status_code == 403

    data = response.json()
    assert data["error"]["code"] == "AUTHORIZATION_ERROR"
    assert "deactivated" in data["error"]["message"].lower()
    assert data["error"]["details"]["account_status"] == "inactive"
