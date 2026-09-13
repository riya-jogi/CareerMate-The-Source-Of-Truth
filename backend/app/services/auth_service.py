from datetime import datetime, timezone
import logging
from typing import Optional, Tuple
import uuid
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.errors import AuthenticationError, ConflictError
from app.core.security import (
    create_access_token,
    create_refresh_token_payload,
    hash_password,
    hash_token,
    verify_password,
)
from app.models.profile import CareerProfile
from app.models.refresh_token import RefreshToken
from app.models.user import User
from app.schemas.auth import UserLoginRequest, UserRegisterRequest

logger = logging.getLogger("careermate.auth")


class AuthService:
    """Service handling candidate authentication, registration, and session logic."""

    @staticmethod
    def register_user(db: Session, request: UserRegisterRequest) -> User:
        """
        Registers a new candidate:
        1. Checks for duplicate email (case-insensitive).
        2. Hashes password using bcrypt.
        3. Creates User record.
        4. Automatically creates the candidate's initial CareerProfile (Source of Truth anchor).
        5. Atomic transaction ensures neither is orphaned.
        """
        normalized_email = request.email.strip().lower()

        # Check existing user
        stmt = select(User).where(User.email == normalized_email)
        existing_user = db.execute(stmt).scalar_one_or_none()
        if existing_user:
            logger.warning(f"Registration attempt with already registered email: {normalized_email}")
            raise ConflictError(
                message="An account with this email address already exists.",
                details={"field": "email"},
            )

        # Hash password with bcrypt
        hashed_password = hash_password(request.password)

        try:
            # 1. Create User
            user = User(
                email=normalized_email,
                hashed_password=hashed_password,
                full_name=request.full_name,
                is_active=True,
                is_verified=False,
            )
            db.add(user)
            db.flush()  # Populates user.id for foreign key

            # 2. Automatically create CareerProfile anchor (Source of Truth principle)
            profile = CareerProfile(
                user_id=user.id,
                headline=request.headline,
            )
            db.add(profile)
            db.flush()

            logger.info(f"Successfully registered user {user.id} and created profile {profile.id}")
            return user

        except IntegrityError as exc:
            db.rollback()
            logger.error(f"Database integrity error during registration: {exc}")
            raise ConflictError(
                message="An account with this email address already exists.",
                details={"field": "email"},
            )

    @staticmethod
    def authenticate_user(
        db: Session,
        request: UserLoginRequest,
        client_ip: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> Tuple[User, str, str]:
        """
        Authenticates a user with email and password:
        - Validates credentials using generic error messages to prevent enumeration.
        - Updates `last_login_at` timestamp.
        - Issues short-lived access token.
        - Issues long-lived revocable refresh token, storing its SHA-256 hash.
        Returns: (user, access_token, raw_refresh_token)
        """
        normalized_email = request.email.strip().lower()

        # Query user
        stmt = select(User).where(User.email == normalized_email)
        user = db.execute(stmt).scalar_one_or_none()

        # Generic failure message to prevent email enumeration
        generic_error = AuthenticationError(
            message="Invalid email or password.",
            details={"field": "credentials"},
        )

        if not user:
            logger.warning(f"Failed login attempt for non-existent email: {normalized_email}")
            raise generic_error

        if not verify_password(request.password, user.hashed_password):
            logger.warning(f"Failed login attempt (bad password) for email: {normalized_email}")
            raise generic_error

        if not user.is_active:
            logger.warning(f"Login attempt for inactive user: {user.id}")
            raise AuthenticationError(
                message="Your account is deactivated. Please contact support.",
                details={"account_status": "inactive"},
            )

        # Update last login timestamp
        user.last_login_at = datetime.now(timezone.utc)

        # Create short-lived access token
        access_token = create_access_token(
            subject=str(user.id),
            claims={"email": user.email},
        )

        # Create and persist revocable refresh token
        raw_refresh, token_hash, expires_at = create_refresh_token_payload()
        token_record = RefreshToken(
            user_id=user.id,
            token_hash=token_hash,
            expires_at=expires_at,
            device_info=user_agent,
            ip_address=client_ip,
        )
        db.add(token_record)
        db.flush()

        logger.info(f"User {user.id} logged in successfully. Session created.")
        return user, access_token, raw_refresh

    @staticmethod
    def refresh_access_token(
        db: Session,
        raw_refresh_token: str,
        client_ip: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> Tuple[str, str]:
        """
        Refreshes an access token using a valid refresh token:
        - Detects token reuse (if a revoked token is used, invalidates ALL user sessions).
        - Enforces refresh token rotation (old token revoked, new one issued).
        Returns: (new_access_token, new_raw_refresh_token)
        """
        if not raw_refresh_token:
            raise AuthenticationError("Refresh token is required.")

        token_hash = hash_token(raw_refresh_token)
        stmt = select(RefreshToken).where(RefreshToken.token_hash == token_hash)
        token_record = db.execute(stmt).scalar_one_or_none()

        if not token_record:
            logger.warning("Refresh attempt with unknown token hash")
            raise AuthenticationError("Invalid or unrecognized refresh token.")

        # Token Reuse Detection (Replay Attack Prevention)
        if token_record.is_revoked:
            logger.critical(
                f"SECURITY ALERT: Revoked refresh token reuse detected for user {token_record.user_id}! "
                f"Invalidating all sessions for this account."
            )
            # Revoke all active tokens for this user
            revoke_stmt = (
                update(RefreshToken)
                .where(RefreshToken.user_id == token_record.user_id)
                .values(is_revoked=True)
            )
            db.execute(revoke_stmt)
            db.commit()
            raise AuthenticationError("Session compromised or revoked. Please sign in again.")

        if token_record.is_expired:
            logger.info(f"Refresh attempt with expired token for user {token_record.user_id}")
            raise AuthenticationError("Refresh token has expired. Please sign in again.")

        # Fetch user
        user = db.get(User, token_record.user_id)
        if not user or not user.is_active:
            raise AuthenticationError("User account not found or deactivated.")

        # 1. Rotate old token (mark revoked)
        token_record.is_revoked = True

        # 2. Issue new refresh token
        new_raw_refresh, new_token_hash, new_expires_at = create_refresh_token_payload()
        new_token_record = RefreshToken(
            user_id=user.id,
            token_hash=new_token_hash,
            expires_at=new_expires_at,
            device_info=user_agent or token_record.device_info,
            ip_address=client_ip or token_record.ip_address,
        )
        db.add(new_token_record)
        db.flush()

        # 3. Issue new access token
        new_access_token = create_access_token(
            subject=str(user.id),
            claims={"email": user.email},
        )

        logger.info(f"Refreshed access token and rotated session for user {user.id}")
        return new_access_token, new_raw_refresh

    @staticmethod
    def revoke_refresh_token(db: Session, raw_refresh_token: str) -> bool:
        """Revokes a specific session/refresh token safely (idempotent)."""
        if not raw_refresh_token:
            return False

        token_hash = hash_token(raw_refresh_token)
        stmt = select(RefreshToken).where(RefreshToken.token_hash == token_hash)
        token_record = db.execute(stmt).scalar_one_or_none()

        if token_record:
            token_record.is_revoked = True
            db.commit()
            logger.info(f"Revoked refresh token session {token_record.id}")
            return True

        return False

    @staticmethod
    def revoke_all_user_sessions(db: Session, user_id: uuid.UUID) -> int:
        """Revokes all active refresh tokens/sessions for a candidate account."""
        stmt = (
            update(RefreshToken)
            .where(RefreshToken.user_id == user_id, RefreshToken.is_revoked == False)
            .values(is_revoked=True)
        )
        result = db.execute(stmt)
        db.commit()
        count = result.rowcount
        logger.info(f"Revoked all {count} active sessions for user {user_id}")
        return count

    @staticmethod
    def get_user_by_id(db: Session, user_id: uuid.UUID) -> Optional[User]:
        """Retrieves a user by UUID."""
        return db.get(User, user_id)


auth_service = AuthService()
