from typing import Annotated, Optional
import uuid
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.errors import AuthenticationError, AuthorizationError
from app.core.security import decode_access_token
from app.db.session import get_db
from app.models.user import User

# Bearer token scheme (auto_error=False allows custom exception handling)
bearer_scheme = HTTPBearer(auto_error=False)

# Type alias for database session dependency
DatabaseSession = Annotated[Session, Depends(get_db)]


def get_current_user(
    db: DatabaseSession,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme),
) -> User:
    """
    Validates Bearer access token from Authorization header and resolves the User entity.
    Raises AuthenticationError (HTTP 401) for missing, malformed, expired, or invalid tokens.
    """
    if not credentials or not credentials.credentials:
        raise AuthenticationError(
            message="Authentication credentials were not provided.",
            details={"auth_scheme": "Bearer"},
        )

    token = credentials.credentials
    try:
        payload = decode_access_token(token)
    except Exception as exc:
        raise AuthenticationError(
            message="Invalid or expired access token.",
            details={"error": str(exc)},
        )

    # Verify token type is 'access'
    token_type = payload.get("type")
    if token_type != "access":
        raise AuthenticationError(
            message="Invalid token type. Access token expected.",
            details={"expected_type": "access", "provided_type": token_type},
        )

    user_id_str = payload.get("sub")
    if not user_id_str:
        raise AuthenticationError(
            message="Malformed token payload.",
            details={"missing_claim": "sub"},
        )

    try:
        user_id = uuid.UUID(user_id_str)
    except ValueError:
        raise AuthenticationError(message="Invalid user identifier in token payload.")

    user = db.get(User, user_id)
    if not user:
        raise AuthenticationError(message="User associated with token no longer exists.")

    return user


def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    """
    Ensures the authenticated candidate's account is active.
    Raises AuthorizationError (HTTP 403 Forbidden) if the account is deactivated.
    """
    if not current_user.is_active:
        raise AuthorizationError(
            message="Your account is deactivated. Please contact support.",
            details={"account_status": "inactive"},
        )
    return current_user


def get_current_verified_user(
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> User:
    """
    Ensures the candidate's account is verified.
    Raises AuthorizationError (HTTP 403 Forbidden) if verification is required.
    """
    if not current_user.is_verified:
        raise AuthorizationError(
            message="Account verification required to access this resource.",
            details={"is_verified": False},
        )
    return current_user


# Primary reusable dependency for all protected endpoints across CareerMate
CurrentUser = Annotated[User, Depends(get_current_active_user)]
VerifiedUser = Annotated[User, Depends(get_current_verified_user)]
