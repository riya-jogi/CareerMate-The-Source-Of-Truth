import uuid
import pytest
from app.core.config import settings
from app.core.security import hash_token
from app.models.refresh_token import RefreshToken


@pytest.fixture
def logged_in_candidate(client):
    """Registers and logs in a test candidate, returning credentials and cookie."""
    email = f"logout_{uuid.uuid4().hex[:8]}@example.com"
    password = "LogoutPass@2026!"
    client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": password, "full_name": "Logout Candidate"},
    )
    login_resp = client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": password},
    )
    assert login_resp.status_code == 200
    raw_refresh = login_resp.cookies[settings.REFRESH_COOKIE_NAME]
    access_token = login_resp.json()["access_token"]
    user_id = login_resp.json()["user"]["id"]

    return {
        "email": email,
        "password": password,
        "access_token": access_token,
        "raw_refresh": raw_refresh,
        "user_id": user_id,
    }


def test_logout_revokes_server_session_and_clears_cookie(client, logged_in_candidate, db_session):
    """1. Invalidate/revoke session and clear cookie."""
    raw_refresh = logged_in_candidate["raw_refresh"]
    token_hash = hash_token(raw_refresh)

    # Verify session active before logout
    db_token = db_session.query(RefreshToken).filter(RefreshToken.token_hash == token_hash).first()
    assert db_token.is_revoked is False

    # Execute logout
    response = client.post(
        "/api/v1/auth/logout",
        cookies={settings.REFRESH_COOKIE_NAME: raw_refresh},
    )
    assert response.status_code == 200
    assert "successfully terminated" in response.json()["message"].lower()

    # Verify session is revoked on server
    db_session.expire_all()
    revoked_token = db_session.query(RefreshToken).filter(RefreshToken.token_hash == token_hash).first()
    assert revoked_token.is_revoked is True


def test_revoked_token_cannot_be_reused_after_logout(client, logged_in_candidate):
    """2. Ensure revoked token cannot be reused to refresh an access token."""
    raw_refresh = logged_in_candidate["raw_refresh"]

    # Log out
    client.post("/api/v1/auth/logout", cookies={settings.REFRESH_COOKIE_NAME: raw_refresh})

    # Attempt to refresh using the revoked token
    refresh_resp = client.post(
        "/api/v1/auth/refresh",
        cookies={settings.REFRESH_COOKIE_NAME: raw_refresh},
    )
    assert refresh_resp.status_code == 401
    assert "compromised or revoked" in refresh_resp.json()["error"]["message"].lower()


def test_logout_idempotent_for_already_revoked_or_missing_tokens(client, logged_in_candidate):
    """3 & 4. Handle already-revoked, expired, or missing sessions gracefully."""
    raw_refresh = logged_in_candidate["raw_refresh"]

    # First logout
    resp1 = client.post("/api/v1/auth/logout", cookies={settings.REFRESH_COOKIE_NAME: raw_refresh})
    assert resp1.status_code == 200

    # Second logout with same revoked token
    resp2 = client.post("/api/v1/auth/logout", cookies={settings.REFRESH_COOKIE_NAME: raw_refresh})
    assert resp2.status_code == 200

    # Logout with completely missing token
    resp3 = client.post("/api/v1/auth/logout")
    assert resp3.status_code == 200


def test_logout_with_explicit_body_payload(client, logged_in_candidate, db_session):
    """5. Logout via explicit request body for clients without cookies."""
    raw_refresh = logged_in_candidate["raw_refresh"]
    token_hash = hash_token(raw_refresh)

    response = client.post(
        "/api/v1/auth/logout",
        json={"refresh_token": raw_refresh},
    )
    assert response.status_code == 200

    db_session.expire_all()
    token_record = db_session.query(RefreshToken).filter(RefreshToken.token_hash == token_hash).first()
    assert token_record.is_revoked is True


def test_logout_all_devices(client, logged_in_candidate, db_session):
    """6. Logout with all_devices=True revokes all active sessions for this candidate."""
    email = logged_in_candidate["email"]
    password = logged_in_candidate["password"]
    user_id = uuid.UUID(logged_in_candidate["user_id"])

    # Create second active session (simulating phone login)
    login_resp_2 = client.post("/api/v1/auth/login", json={"email": email, "password": password})
    raw_refresh_2 = login_resp_2.cookies[settings.REFRESH_COOKIE_NAME]

    # Verify both sessions active
    active_tokens_before = (
        db_session.query(RefreshToken)
        .filter(RefreshToken.user_id == user_id, RefreshToken.is_revoked == False)
        .all()
    )
    assert len(active_tokens_before) == 2

    # Logout with all_devices=True
    logout_all_resp = client.post(
        "/api/v1/auth/logout",
        json={"refresh_token": raw_refresh_2, "all_devices": True},
    )
    assert logout_all_resp.status_code == 200
    assert "all" in logout_all_resp.json()["message"].lower()

    # Verify all sessions are revoked on server
    db_session.expire_all()
    active_tokens_after = (
        db_session.query(RefreshToken)
        .filter(RefreshToken.user_id == user_id, RefreshToken.is_revoked == False)
        .all()
    )
    assert len(active_tokens_after) == 0
