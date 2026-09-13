from datetime import datetime
import re
from typing import Optional
import uuid
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class UserRegisterRequest(BaseModel):
    """Payload for registering a new candidate account."""

    email: EmailStr = Field(
        ...,
        description="Candidate's email address (will be normalized to lowercase)",
        examples=["candidate@example.com"],
    )
    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="Password must be 8-128 chars, containing uppercase, lowercase, digit, and symbol",
        examples=["StrongPass@2026!"],
    )
    full_name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Candidate's legal or professional full name",
        examples=["Alex Mercer"],
    )
    headline: Optional[str] = Field(
        default=None,
        max_length=255,
        description="Optional initial professional headline (e.g., 'Senior AI Engineer')",
        examples=["Senior AI Platform Engineer"],
    )

    @field_validator("email", mode="before")
    @classmethod
    def normalize_email(cls, v: str) -> str:
        if isinstance(v, str):
            return v.strip().lower()
        return v

    @field_validator("full_name", mode="before")
    @classmethod
    def clean_full_name(cls, v: str) -> str:
        if isinstance(v, str):
            cleaned = v.strip()
            if len(cleaned) < 2:
                raise ValueError("Full name must contain at least 2 non-whitespace characters")
            return cleaned
        return v

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter (A-Z)")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter (a-z)")
        if not re.search(r"[0-9]", v):
            raise ValueError("Password must contain at least one digit (0-9)")
        if not re.search(r"[!@#$%^&*()_+\-=\[\]{}|;:,.<>?~`]", v):
            raise ValueError("Password must contain at least one special character (!@#$%^&*...)")
        return v


class CareerProfileSummaryResponse(BaseModel):
    """Public summary of the candidate's Career Profile."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    headline: Optional[str] = None
    summary: Optional[str] = None
    location: Optional[str] = None
    created_at: datetime


class UserRegisterResponse(BaseModel):
    """
    Public response after successful candidate registration.
    Security guarantee: NEVER returns password hashes or authentication secrets.
    """

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    email: str
    full_name: str
    is_active: bool
    is_verified: bool
    created_at: datetime
    career_profile: Optional[CareerProfileSummaryResponse] = None
    message: str = "Candidate registered successfully. Career profile anchor created."


class UserLoginRequest(BaseModel):
    """Payload for candidate authentication."""

    email: EmailStr = Field(..., description="Registered email address")
    password: str = Field(..., min_length=1, description="Account password")

    @field_validator("email", mode="before")
    @classmethod
    def normalize_email(cls, v: str) -> str:
        if isinstance(v, str):
            return v.strip().lower()
        return v


class UserResponse(BaseModel):
    """Public user details model."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    email: str
    full_name: str
    is_active: bool
    is_verified: bool
    last_login_at: Optional[datetime] = None
    created_at: datetime
    career_profile: Optional[CareerProfileSummaryResponse] = None


class LoginResponse(BaseModel):
    """
    Response returned upon successful login.
    The short-lived access token is returned in the payload for Authorization header.
    The long-lived refresh token is securely set in an HttpOnly cookie.
    """

    access_token: str = Field(..., description="Short-lived JWT access token")
    token_type: str = "bearer"
    expires_in: int = Field(..., description="Access token expiration duration in seconds")
    user: UserResponse


class RefreshTokenRequest(BaseModel):
    """Optional payload for clients unable to use HttpOnly cookies (e.g. mobile apps)."""

    refresh_token: Optional[str] = Field(None, description="Explicit refresh token string")


class TokenRefreshResponse(BaseModel):
    """Response containing a new short-lived access token."""

    access_token: str
    token_type: str = "bearer"
    expires_in: int


class LogoutRequest(BaseModel):
    """Optional payload for logout requests."""

    refresh_token: Optional[str] = Field(None, description="Explicit refresh token string")
    all_devices: bool = Field(False, description="If true, revokes all active sessions for this account")


class LogoutResponse(BaseModel):
    """Response confirming session revocation."""

    message: str = "Session successfully terminated."

