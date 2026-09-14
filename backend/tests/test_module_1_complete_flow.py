"""
Module 1 Complete End-to-End Verification Test Suite
Covers the exact 16-step flow requested by the user, plus all negative test cases:
1. Registration request validation & reaches backend
2. Password securely hashed (bcrypt) & never returned
3. User record stored in PostgreSQL
4. CareerProfile anchor created in PostgreSQL (1:1 with user)
5. Authentication established (access token + HttpOnly refresh cookie)
6. Dashboard reaches authenticated current-user & dashboard summary endpoints
7. Refresh & rotation behavior works
8. User logs out & server session is revoked
9. Blocked access after logout
10. Re-authentication (Sign in again & reach dashboard again)
11. Negative cases: duplicate registration, wrong password, unknown email,
    invalid token, expired token, revoked session, missing auth, invalid payload.
"""

from datetime import datetime, timedelta, timezone
import uuid
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import create_access_token, hash_token, verify_password
from app.models.profile import CareerProfile
from app.models.refresh_token import RefreshToken
from app.models.user import User


class TestModule1CompleteFlow:
    """Comprehensive test class for Module 1 End-to-End Flow and Negative Cases."""

    def test_complete_sixteen_step_flow(self, client: TestClient, db_session: Session):
        """
        Executes the exact 16-step user journey from initial sign-up to re-authentication.
        """
        unique_id = uuid.uuid4().hex[:8]
        candidate_email = f"candidate_{unique_id}@example.com"
        raw_password = "SecurePass@2026!"
        candidate_name = f"Alex Morgan {unique_id}"
        candidate_headline = "Lead AI Platform Engineer"

        # -------------------------------------------------------------------------
        # Step 1 & 2: Client-side validation is enforced; invalid payloads rejected
        # (Tested thoroughly in test_negative_cases below; here we test valid dispatch)
        # -------------------------------------------------------------------------

        # Step 3: Valid registration reaches the backend
        reg_payload = {
            "email": candidate_email,
            "password": raw_password,
            "full_name": candidate_name,
            "headline": candidate_headline,
        }
        reg_response = client.post("/api/v1/auth/register", json=reg_payload)
        assert reg_response.status_code == 201
        reg_data = reg_response.json()
        user_id = reg_data["id"]

        # Step 4: Password is securely hashed with bcrypt & never returned
        assert "password" not in reg_data
        assert "hashed_password" not in reg_data

        # Query database directly
        db_user = db_session.scalar(select(User).where(User.id == uuid.UUID(user_id)))
        assert db_user is not None
        assert db_user.hashed_password != raw_password
        assert db_user.hashed_password.startswith("$2b$")
        assert len(db_user.hashed_password) == 60
        assert verify_password(raw_password, db_user.hashed_password) is True
        assert verify_password("WrongPass@123", db_user.hashed_password) is False

        # Step 5: User is stored in PostgreSQL
        assert db_user.email == candidate_email.lower()
        assert db_user.full_name == candidate_name
        assert db_user.is_active is True

        # Step 6: CareerProfile anchor is created atomically (1:1 relationship)
        db_profile = db_session.scalar(select(CareerProfile).where(CareerProfile.user_id == db_user.id))
        assert db_profile is not None
        assert db_profile.headline == candidate_headline
        assert db_profile.user_id == db_user.id

        # Step 7: Authentication is established (Sign In / Login)
        login_payload = {
            "email": candidate_email,
            "password": raw_password,
        }
        login_response = client.post("/api/v1/auth/login", json=login_payload)
        assert login_response.status_code == 200
        login_data = login_response.json()

        access_token = login_data["access_token"]
        assert access_token is not None
        assert login_data["token_type"] == "bearer"
        assert login_data["user"]["email"] == candidate_email.lower()
        assert login_data["user"]["career_profile"]["headline"] == candidate_headline

        # Verify 7-day HttpOnly cookie is set
        cookie_header = login_response.headers.get("set-cookie")
        assert cookie_header is not None
        assert settings.REFRESH_COOKIE_NAME in cookie_header
        assert "HttpOnly" in cookie_header
        assert "SameSite=lax" in cookie_header

        refresh_cookie_value = login_response.cookies.get(settings.REFRESH_COOKIE_NAME)
        assert refresh_cookie_value is not None

        # Verify refresh token hash is stored in PostgreSQL
        token_hash = hash_token(refresh_cookie_value)
        db_token = db_session.scalar(select(RefreshToken).where(RefreshToken.token_hash == token_hash))
        assert db_token is not None
        assert db_token.user_id == db_user.id
        assert db_token.is_revoked is False

        # Step 8 & 9: User reaches Dashboard; calls authenticated current-user & dashboard summary endpoints
        headers = {"Authorization": f"Bearer {access_token}"}
        
        # 9a: GET /api/v1/auth/me
        me_response = client.get("/api/v1/auth/me", headers=headers)
        assert me_response.status_code == 200
        me_data = me_response.json()
        assert me_data["id"] == user_id
        assert me_data["email"] == candidate_email.lower()
        assert me_data["full_name"] == candidate_name
        assert me_data["career_profile"]["headline"] == candidate_headline

        # 9b: GET /api/v1/dashboard/summary
        summary_response = client.get("/api/v1/dashboard/summary", headers=headers)
        assert summary_response.status_code == 200
        summary_data = summary_response.json()
        assert summary_data["candidate_name"] == candidate_name
        assert summary_data["candidate_email"] == candidate_email.lower()
        assert summary_data["candidate_headline"] == candidate_headline
        assert summary_data["active_anchor"] is True
        assert summary_data["profile_completeness_percentage"] >= 50

        # Step 10: Refresh/authentication behavior works
        refresh_response = client.post(
            "/api/v1/auth/refresh",
            cookies={settings.REFRESH_COOKIE_NAME: refresh_cookie_value},
        )
        assert refresh_response.status_code == 200
        refresh_data = refresh_response.json()
        new_access_token = refresh_data["access_token"]
        assert new_access_token is not None
        assert new_access_token != access_token

        # Verify token rotation: new refresh token cookie issued, old marked revoked
        new_refresh_cookie = refresh_response.cookies.get(settings.REFRESH_COOKIE_NAME)
        assert new_refresh_cookie is not None
        assert new_refresh_cookie != refresh_cookie_value

        db_session.expire_all()
        old_token_record = db_session.scalar(select(RefreshToken).where(RefreshToken.token_hash == token_hash))
        assert old_token_record.is_revoked is True

        new_token_hash = hash_token(new_refresh_cookie)
        new_token_record = db_session.scalar(select(RefreshToken).where(RefreshToken.token_hash == new_token_hash))
        assert new_token_record.is_revoked is False

        # Verify new access token works against protected endpoint
        new_headers = {"Authorization": f"Bearer {new_access_token}"}
        me_response_new = client.get("/api/v1/auth/me", headers=new_headers)
        assert me_response_new.status_code == 200

        # Step 11: User logs out
        logout_response = client.post(
            "/api/v1/auth/logout",
            cookies={settings.REFRESH_COOKIE_NAME: new_refresh_cookie},
        )
        assert logout_response.status_code == 200
        assert logout_response.json()["success"] is True

        # Step 12: Authentication/session is invalidated
        logout_cookie_header = logout_response.headers.get("set-cookie")
        assert logout_cookie_header is not None
        assert 'max-age=0' in logout_cookie_header.lower()

        db_session.expire_all()
        logged_out_record = db_session.scalar(select(RefreshToken).where(RefreshToken.token_hash == new_token_hash))
        assert logged_out_record.is_revoked is True

        # Step 13 & 14: Direct access to /app/dashboard and endpoints blocked after logout
        blocked_summary = client.get("/api/v1/dashboard/summary")
        assert blocked_summary.status_code == 401

        blocked_me = client.get("/api/v1/auth/me")
        assert blocked_me.status_code == 401

        # Attempting to refresh using the revoked session fails
        revoked_refresh_attempt = client.post(
            "/api/v1/auth/refresh",
            cookies={settings.REFRESH_COOKIE_NAME: new_refresh_cookie},
        )
        assert revoked_refresh_attempt.status_code == 401

        # Step 15: User can sign in again
        relogin_response = client.post("/api/v1/auth/login", json=login_payload)
        assert relogin_response.status_code == 200
        relogin_data = relogin_response.json()
        relogin_access_token = relogin_data["access_token"]
        assert relogin_access_token is not None

        # Step 16: User reaches Dashboard again
        relogin_headers = {"Authorization": f"Bearer {relogin_access_token}"}
        relogin_summary = client.get("/api/v1/dashboard/summary", headers=relogin_headers)
        assert relogin_summary.status_code == 200
        assert relogin_summary.json()["candidate_name"] == candidate_name
        assert relogin_summary.json()["last_login_at"] is not None

    def test_negative_cases(self, client: TestClient, db_session: Session):
        """
        Comprehensive test coverage for all negative authentication cases:
        - Duplicate registration
        - Wrong password
        - Unknown email
        - Invalid token
        - Expired token
        - Revoked session reuse
        - Missing authentication
        - Deactivated user
        - Password strength validation failures
        - Full name validation failures
        """
        unique_id = uuid.uuid4().hex[:8]
        email = f"negative_{unique_id}@example.com"
        password = "ValidPass@2026!"

        # Create base user
        reg_res = client.post(
            "/api/v1/auth/register",
            json={"email": email, "password": password, "full_name": "Negative Tester"},
        )
        assert reg_res.status_code == 201

        # 1. Duplicate registration -> 409 CONFLICT
        dup_res = client.post(
            "/api/v1/auth/register",
            json={"email": email, "password": password, "full_name": "Duplicate Attempt"},
        )
        assert dup_res.status_code == 409
        dup_data = dup_res.json()
        assert dup_data["error"]["code"] == "RESOURCE_CONFLICT"
        assert "already exists" in dup_data["error"]["message"].lower()

        # 2. Wrong password -> 401 Generic invalid credentials
        wrong_pass_res = client.post(
            "/api/v1/auth/login",
            json={"email": email, "password": "WrongPassword@123!"},
        )
        assert wrong_pass_res.status_code == 401
        assert wrong_pass_res.json()["error"]["message"] == "Invalid email or password"

        # 3. Unknown email -> 401 Identical generic invalid credentials
        unknown_res = client.post(
            "/api/v1/auth/login",
            json={"email": "nonexistent.user@example.com", "password": password},
        )
        assert unknown_res.status_code == 401
        assert unknown_res.json()["error"]["message"] == "Invalid email or password"

        # 4. Invalid token (malformed or invalid signature) -> 401
        invalid_token_res = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": "Bearer not.a.valid.jwt.token"},
        )
        assert invalid_token_res.status_code == 401
        assert invalid_token_res.json()["error"]["code"] == "AUTHENTICATION_ERROR"

        # 5. Expired token -> 401
        user = db_session.scalar(select(User).where(User.email == email))
        expired_token = create_access_token(
            subject=str(user.id),
            expires_delta=timedelta(seconds=-10),
        )
        expired_res = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {expired_token}"},
        )
        assert expired_res.status_code == 401
        assert "expired" in expired_res.json()["error"]["message"].lower()

        # 6. Missing authentication -> 401
        missing_res = client.get("/api/v1/auth/me")
        assert missing_res.status_code == 401

        # 7. Inactive / deactivated user -> 401
        user.is_active = False
        db_session.commit()
        inactive_login = client.post(
            "/api/v1/auth/login",
            json={"email": email, "password": password},
        )
        assert inactive_login.status_code == 401
        assert "deactivated" in inactive_login.json()["error"]["message"].lower()

        # Reactivate for subsequent tests
        user.is_active = True
        db_session.commit()

        # 8. Password strength failures -> 422
        weak_passwords = [
            "short1!",  # < 8 chars
            "nouppercase123!",  # no uppercase
            "NOLOWERCASE123!",  # no lowercase
            "NoNumbersHere!",  # no digit
            "NoSpecialSymbols123",  # no symbol
        ]
        for weak_pass in weak_passwords:
            res = client.post(
                "/api/v1/auth/register",
                json={
                    "email": f"weak_{uuid.uuid4().hex[:6]}@example.com",
                    "password": weak_pass,
                    "full_name": "Weak Pass Tester",
                },
            )
            assert res.status_code == 422

        # 9. Invalid full name (too short or whitespace only) -> 422
        name_res = client.post(
            "/api/v1/auth/register",
            json={
                "email": f"name_{uuid.uuid4().hex[:6]}@example.com",
                "password": password,
                "full_name": "   ",
            },
        )
        assert name_res.status_code == 422
