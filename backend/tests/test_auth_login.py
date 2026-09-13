import uuid
import pytest
from app.core.config import settings
from app.core.security import hash_token
from app.models.refresh_token import RefreshToken
from app.models.user import User


@pytest.fixture
def registered_user(client):
    """Registers a fresh test user and returns credentials."""
    email = f"logintest_{uuid.uuid4().hex[:8]}@example.com"
    password = "SecurePassword@2026!"
    payload = {
        "email": email,
        "password": password,
        "full_name": "Login Test Candidate",
        "headline": "Lead Full-Stack AI Engineer",
    }
    resp = client.post("/api/v1/auth/register", json=payload)
    assert resp.status_code == 201
    return {"email": email, "password": password, "user_id": resp.json()["id"]}


def test_login_success(client, registered_user, db_session):
    login_payload = {
        "email": registered_user["email"],
        "password": registered_user["password"],
    }
    response = client.post("/api/v1/auth/login", json=login_payload)
    assert response.status_code == 200

    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["expires_in"] == settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60

    # User details & last_login_at updated
    assert data["user"]["email"] == registered_user["email"].lower()
    assert data["user"]["last_login_at"] is not None

    # Verify HttpOnly Cookie is set
    assert settings.REFRESH_COOKIE_NAME in response.cookies
    raw_refresh = response.cookies[settings.REFRESH_COOKIE_NAME]
    assert len(raw_refresh) > 20

    # Verify RefreshToken record in DB
    token_hash = hash_token(raw_refresh)
    db_token = db_session.query(RefreshToken).filter(RefreshToken.token_hash == token_hash).first()
    assert db_token is not None
    assert db_token.is_revoked is False
    assert db_token.is_active is True


def test_login_invalid_password_returns_generic_401(client, registered_user):
    login_payload = {
        "email": registered_user["email"],
        "password": "WrongPassword999!",
    }
    response = client.post("/api/v1/auth/login", json=login_payload)
    assert response.status_code == 401

    data = response.json()
    assert data["error"]["code"] == "AUTHENTICATION_ERROR"
    assert "invalid email or password" in data["error"]["message"].lower()


def test_login_nonexistent_user_returns_identical_generic_401(client):
    login_payload = {
        "email": "nonexistent_candidate_999@example.com",
        "password": "AnyPassword123!",
    }
    response = client.post("/api/v1/auth/login", json=login_payload)
    assert response.status_code == 401

    data = response.json()
    assert data["error"]["code"] == "AUTHENTICATION_ERROR"
    # Generic error message must match invalid password exactly to prevent enumeration
    assert "invalid email or password" in data["error"]["message"].lower()


def test_login_inactive_user_returns_401(client, registered_user, db_session):
    # Deactivate user in DB
    user = db_session.get(User, uuid.UUID(registered_user["user_id"]))
    user.is_active = False
    db_session.commit()

    login_payload = {
        "email": registered_user["email"],
        "password": registered_user["password"],
    }
    response = client.post("/api/v1/auth/login", json=login_payload)
    assert response.status_code == 401
    data = response.json()
    assert "deactivated" in data["error"]["message"].lower()


def test_refresh_token_rotation(client, registered_user, db_session):
    login_resp = client.post(
        "/api/v1/auth/login",
        json={"email": registered_user["email"], "password": registered_user["password"]},
    )
    old_raw_refresh = login_resp.cookies[settings.REFRESH_COOKIE_NAME]

    # Call /refresh endpoint using cookie
    refresh_resp = client.post("/api/v1/auth/refresh", cookies={settings.REFRESH_COOKIE_NAME: old_raw_refresh})
    assert refresh_resp.status_code == 200

    data = refresh_resp.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

    # New rotated cookie must be issued
    new_raw_refresh = refresh_resp.cookies[settings.REFRESH_COOKIE_NAME]
    assert new_raw_refresh != old_raw_refresh

    # Old token must now be marked is_revoked = True in DB
    old_token_hash = hash_token(old_raw_refresh)
    old_db_token = db_session.query(RefreshToken).filter(RefreshToken.token_hash == old_token_hash).first()
    assert old_db_token.is_revoked is True


def test_refresh_token_reuse_detection_revokes_all_sessions(client, registered_user, db_session):
    login_resp = client.post(
        "/api/v1/auth/login",
        json={"email": registered_user["email"], "password": registered_user["password"]},
    )
    old_raw_refresh = login_resp.cookies[settings.REFRESH_COOKIE_NAME]

    # Legitimate first refresh (rotates old token)
    client.post("/api/v1/auth/refresh", cookies={settings.REFRESH_COOKIE_NAME: old_raw_refresh})

    # MALICIOUS SECOND ATTEMPT: Attempt to reuse the already-rotated (revoked) token!
    reuse_resp = client.post("/api/v1/auth/refresh", cookies={settings.REFRESH_COOKIE_NAME: old_raw_refresh})
    assert reuse_resp.status_code == 401
    assert "compromised" in reuse_resp.json()["error"]["message"].lower()

    # Verify all tokens for this user have been invalidated
    user_id = uuid.UUID(registered_user["user_id"])
    active_tokens = (
        db_session.query(RefreshToken)
        .filter(RefreshToken.user_id == user_id, RefreshToken.is_revoked == False)
        .all()
    )
    assert len(active_tokens) == 0


def test_logout_revokes_session_and_clears_cookie(client, registered_user, db_session):
    login_resp = client.post(
        "/api/v1/auth/login",
        json={"email": registered_user["email"], "password": registered_user["password"]},
    )
    raw_refresh = login_resp.cookies[settings.REFRESH_COOKIE_NAME]

    logout_resp = client.post("/api/v1/auth/logout", cookies={settings.REFRESH_COOKIE_NAME: raw_refresh})
    assert logout_resp.status_code == 200
    assert "successfully terminated" in logout_resp.json()["message"].lower()

    # Verify token revoked in DB
    token_hash = hash_token(raw_refresh)
    token_record = db_session.query(RefreshToken).filter(RefreshToken.token_hash == token_hash).first()
    assert token_record.is_revoked is True


def test_get_current_user_me_endpoint(client, registered_user):
    # 1. Login to obtain access token
    login_resp = client.post(
        "/api/v1/auth/login",
        json={"email": registered_user["email"], "password": registered_user["password"]},
    )
    access_token = login_resp.json()["access_token"]

    # 2. Access /me with Bearer token
    me_resp = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert me_resp.status_code == 200
    me_data = me_resp.json()
    assert me_data["email"] == registered_user["email"].lower()
    assert me_data["career_profile"]["headline"] == "Lead Full-Stack AI Engineer"

    # 3. Access /me without token -> 401
    unauth_resp = client.get("/api/v1/auth/me")
    assert unauth_resp.status_code == 401

    # 4. Access /me with invalid token -> 401
    invalid_resp = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": "Bearer invalid.jwt.token"},
    )
    assert invalid_resp.status_code == 401
