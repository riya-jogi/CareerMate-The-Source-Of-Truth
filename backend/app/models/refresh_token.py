from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional
import uuid
from sqlalchemy import Boolean, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from app.models.user import User


class RefreshToken(Base, UUIDMixin, TimestampMixin):
    """
    RefreshToken entity: Stores cryptographically hashed refresh tokens/sessions.
    Enables secure token rotation, device tracking, and explicit session revocation
    without storing plaintext tokens in the database.
    """

    __tablename__ = "refresh_tokens"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    token_hash: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        index=True,
        nullable=False,
    )
    is_revoked: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        index=True,
    )
    device_info: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )
    ip_address: Mapped[Optional[str]] = mapped_column(
        String(45),
        nullable=True,
    )

    # Many-to-1 relationship back to User
    user: Mapped["User"] = relationship(
        "User",
        back_populates="refresh_tokens",
    )

    @property
    def is_expired(self) -> bool:
        """Determines if the token has passed its expiration time."""
        return datetime.now(timezone.utc) >= self.expires_at

    @property
    def is_active(self) -> bool:
        """Determines if the token is valid for refreshing an access token."""
        return (not self.is_revoked) and (not self.is_expired)

    def __repr__(self) -> str:
        return f"<RefreshToken(id={self.id}, user_id={self.user_id}, is_revoked={self.is_revoked})>"
