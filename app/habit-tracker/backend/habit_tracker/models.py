"""SQLAlchemy models for the habit tracker.

Cadence is stored as a short string rather than a native PostgreSQL enum.
Pydantic already restricts the accepted values, and a plain column keeps later
schema migrations simple: adding a cadence becomes an application change rather
than an enum type alteration.
"""

from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from habit_tracker.schemas import MAX_DESCRIPTION_LENGTH, MAX_NAME_LENGTH

CADENCE_LENGTH = 16
DISPLAY_NAME_LENGTH = 100


def _utc_now() -> datetime:
    return datetime.now(UTC)


class Base(DeclarativeBase):
    """Declarative base shared by every model."""


class User(Base):
    """A person who owns habits.

    Authentication arrives in a later milestone. Until then the service seeds a
    single user and treats it as the owner of everything.
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    display_name: Mapped[str] = mapped_column(String(DISPLAY_NAME_LENGTH))
    total_points: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utc_now, server_default=func.now()
    )

    habits: Mapped[list[Habit]] = relationship(
        back_populates="owner", cascade="all, delete-orphan"
    )


class Habit(Base):
    """A recurring activity worth points when completed."""

    __tablename__ = "habits"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    name: Mapped[str] = mapped_column(String(MAX_NAME_LENGTH))
    description: Mapped[str | None] = mapped_column(
        String(MAX_DESCRIPTION_LENGTH), nullable=True
    )
    cadence: Mapped[str] = mapped_column(String(CADENCE_LENGTH))
    points_per_completion: Mapped[int] = mapped_column(Integer)
    is_archived: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default="false"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utc_now, server_default=func.now()
    )

    owner: Mapped[User] = relationship(back_populates="habits")
