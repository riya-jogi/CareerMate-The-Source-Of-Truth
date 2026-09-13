from typing import Optional, Union
from fastapi import APIRouter, Request, Response, status

from app.api.deps import CurrentUser, DatabaseSession
from app.core.config import settings
from app.core.errors import AuthenticationError
from app.core.security import hash_token
from app.schemas.auth import (
    LoginResponse,
    LogoutRequest,
    LogoutResponse,
    RefreshTokenRequest,
    TokenRefreshResponse,
    UserLoginRequest,
    UserRegisterRequest,
    UserRegisterResponse,
    UserResponse,
)
from app.services.auth_service import auth_service

router = APIRouter(prefix="/auth", tags=["Authentication"])


def _extract_refresh_token(request: Request, body: Optional[Union[RefreshTokenRequest, LogoutRequest]] = None) -> Optional[str]:
    """Extracts refresh token from HttpOnly cookie first, then fallback to request body."""
    cookie_token = request.cookies.get(settings.REFRESH_COOKIE_NAME)
    if cookie_token:
        return cookie_token
    if body and body.refresh_token:
        return body.refresh_token
    return None


@router.post(
    "/register",
    response_model=UserRegisterResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register Candidate Account",
    description=(
        "Registers a new candidate account with email and strong password. "
        "Automatically provisions the candidate's initial CareerProfile anchor "
        "in an atomic transaction. Never returns password hashes."
    ),
)
def register(
    payload: UserRegisterRequest,
    db: DatabaseSession,
) -> UserRegisterResponse:
    user = auth_service.register_user(db=db, request=payload)
    return UserRegisterResponse.model_validate(user)


@router.post(
    "/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
    summary="Candidate Login",
    description=(
        "Authenticates a candidate using email and password. Returns a short-lived "
        "JWT access token (15 mins) and sets a secure HttpOnly refresh token cookie (7 days). "
        "Updates candidate last_login_at timestamp."
    ),
)
def login(
    payload: UserLoginRequest,
    request: Request,
    response: Response,
    db: DatabaseSession,
) -> LoginResponse:
    client_ip = request.client.host if request.client else None
    user_agent = request.headers.get("user-agent")

    user, access_token, raw_refresh = auth_service.authenticate_user(
        db=db,
        request=payload,
        client_ip=client_ip,
        user_agent=user_agent,
    )

    # Set secure HttpOnly cookie for refresh token (avoids localStorage XSS vulnerabilities)
    response.set_cookie(
        key=settings.REFRESH_COOKIE_NAME,
        value=raw_refresh,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite=settings.COOKIE_SAMESITE,
        path=settings.REFRESH_COOKIE_PATH,
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 86400,
    )

    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user=UserResponse.model_validate(user),
    )


@router.post(
    "/refresh",
    response_model=TokenRefreshResponse,
    status_code=status.HTTP_200_OK,
    summary="Refresh Access Token",
    description=(
        "Exchanges a valid refresh token for a new short-lived access token. "
        "Enforces refresh token rotation and rotates the HttpOnly cookie. "
        "Revoked token reuse triggers automatic invalidation of all user sessions."
    ),
)
def refresh_token(
    request: Request,
    response: Response,
    db: DatabaseSession,
    body: Optional[RefreshTokenRequest] = None,
) -> TokenRefreshResponse:
    raw_refresh = _extract_refresh_token(request, body)
    if not raw_refresh:
        raise AuthenticationError(
            message="No refresh token provided in cookie or payload.",
            details={"source": "cookie_or_body"},
        )

    client_ip = request.client.host if request.client else None
    user_agent = request.headers.get("user-agent")

    new_access_token, new_raw_refresh = auth_service.refresh_access_token(
        db=db,
        raw_refresh_token=raw_refresh,
        client_ip=client_ip,
        user_agent=user_agent,
    )

    # Rotate cookie with newly issued refresh token
    response.set_cookie(
        key=settings.REFRESH_COOKIE_NAME,
        value=new_raw_refresh,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite=settings.COOKIE_SAMESITE,
        path=settings.REFRESH_COOKIE_PATH,
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 86400,
    )

    return TokenRefreshResponse(
        access_token=new_access_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )


@router.post(
    "/logout",
    response_model=LogoutResponse,
    status_code=status.HTTP_200_OK,
    summary="Logout and Terminate Session",
    description=(
        "Safely revokes the active refresh token session in the database and clears "
        "the HttpOnly cookie. Handles already expired/revoked sessions idempotently. "
        "Optionally revokes all active sessions across all devices."
    ),
)
def logout(
    request: Request,
    response: Response,
    db: DatabaseSession,
    body: Optional[LogoutRequest] = None,
) -> LogoutResponse:
    # 1. Clear HttpOnly cookie on client regardless of whether token exists
    response.delete_cookie(
        key=settings.REFRESH_COOKIE_NAME,
        path=settings.REFRESH_COOKIE_PATH,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite=settings.COOKIE_SAMESITE,
    )

    all_devices = body.all_devices if body else False
    raw_refresh = _extract_refresh_token(request, body)

    if raw_refresh:
        token_hash = hash_token(raw_refresh)
        # Find token to identify user if all_devices requested
        from sqlalchemy import select
        from app.models.refresh_token import RefreshToken
        token_record = db.execute(select(RefreshToken).where(RefreshToken.token_hash == token_hash)).scalar_one_or_none()

        if token_record:
            if all_devices:
                count = auth_service.revoke_all_user_sessions(db=db, user_id=token_record.user_id)
                return LogoutResponse(message=f"All {count} active sessions terminated successfully.")
            else:
                auth_service.revoke_refresh_token(db=db, raw_refresh_token=raw_refresh)

    return LogoutResponse(message="Session successfully terminated.")


@router.get(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Current Authenticated Candidate",
    description="Retrieves profile and account information for the currently authenticated user.",
)
def get_current_user_profile(
    current_user: CurrentUser,
) -> UserResponse:
    return UserResponse.model_validate(current_user)
