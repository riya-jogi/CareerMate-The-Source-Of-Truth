from datetime import datetime, timedelta, timezone
import hashlib
import uuid
import pytest
from sqlalchemy.exc import IntegrityError

from app.models.user import User
from app.models.profile import CareerProfile
from app.models.refresh_token import RefreshToken
from app.core.security import hash_password


def test_user_and_career_profile_creation(db_session):
    unique_email = f"candidate_{uuid.uuid4().hex[:8]}@example.com"
    user = User(
        email=unique_email,
        hashed_password=hash_password("Secret123!"),
        full_name="Alex Mercer",
    )
    db_session.add(user)
    db_session.flush()

    assert user.id is not None
    assert user.email == unique_email
    assert user.is_active is True
    assert user.is_verified is False

    # Create associated Career Profile (source of truth anchor)
    profile = CareerProfile(
        user_id=user.id,
        headline="Senior AI Platform Engineer",
        summary="Specializing in trustworthy candidate ATS optimization.",
        location="San Francisco, CA",
    )
    db_session.add(profile)
    db_session.flush()

    assert profile.id is not None
    assert profile.user_id == user.id
    assert user.career_profile.headline == "Senior AI Platform Engineer"
    assert profile.user.email == unique_email


def test_refresh_token_lifecycle_and_relationships(db_session):
    unique_email = f"session_user_{uuid.uuid4().hex[:8]}@example.com"
    user = User(
        email=unique_email,
        hashed_password=hash_password("StrongPass123!"),
        full_name="Session Candidate",
    )
    db_session.add(user)
    db_session.flush()

    # Create active refresh token
    token_raw = uuid.uuid4().hex
    token_hash = hashlib.sha256(token_raw.encode("utf-8")).hexdigest()
    expires_at = datetime.now(timezone.utc) + timedelta(days=7)

    refresh_token = RefreshToken(
        user_id=user.id,
        token_hash=token_hash,
        expires_at=expires_at,
        device_info="Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        ip_address="127.0.0.1",
    )
    db_session.add(refresh_token)
    db_session.flush()

    assert refresh_token.id is not None
    assert refresh_token.user_id == user.id
    assert refresh_token.is_revoked is False
    assert refresh_token.is_expired is False
    assert refresh_token.is_active is True
    assert len(user.refresh_tokens) == 1
    assert user.refresh_tokens[0].token_hash == token_hash

    # Test revocation
    refresh_token.is_revoked = True
    assert refresh_token.is_active is False


def test_cascade_delete_removes_profile_and_tokens(db_session):
    unique_email = f"cascade_{uuid.uuid4().hex[:8]}@example.com"
    user = User(
        email=unique_email,
        hashed_password=hash_password("Pass123!"),
        full_name="Cascade Candidate",
    )
    db_session.add(user)
    db_session.flush()

    profile = CareerProfile(user_id=user.id, headline="Engineer")
    db_session.add(profile)

    token = RefreshToken(
        user_id=user.id,
        token_hash=hashlib.sha256(uuid.uuid4().bytes).hexdigest(),
        expires_at=datetime.now(timezone.utc) + timedelta(days=1),
    )
    db_session.add(token)
    db_session.flush()

    user_id = user.id
    profile_id = profile.id
    token_id = token.id

    # Delete the user
    db_session.delete(user)
    db_session.flush()

    # Verify associated profile and tokens were automatically deleted
    assert db_session.get(User, user_id) is None
    assert db_session.get(CareerProfile, profile_id) is None
    assert db_session.get(RefreshToken, token_id) is None


def test_duplicate_email_raises_integrity_error(db_session):
    duplicate_email = f"duplicate_{uuid.uuid4().hex[:8]}@example.com"
    user1 = User(email=duplicate_email, hashed_password="h1", full_name="User 1")
    db_session.add(user1)
    db_session.flush()

    user2 = User(email=duplicate_email, hashed_password="h2", full_name="User 2")
    db_session.add(user2)

    with pytest.raises(IntegrityError):
        db_session.flush()
    db_session.rollback()
