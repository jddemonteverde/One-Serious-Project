"""Request and response models for the habits API."""

from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, field_validator

MAX_NAME_LENGTH = 100
MAX_DESCRIPTION_LENGTH = 500
MIN_POINTS_PER_COMPLETION = 1
MAX_POINTS_PER_COMPLETION = 100
DEFAULT_POINTS_PER_COMPLETION = 10


class Cadence(str, Enum):
    """How often a habit is expected to be completed."""

    DAILY = "daily"
    WEEKLY = "weekly"


class HabitFields(BaseModel):
    """Fields a client supplies when creating or replacing a habit."""

    name: str = Field(min_length=1, max_length=MAX_NAME_LENGTH)
    description: str | None = Field(default=None, max_length=MAX_DESCRIPTION_LENGTH)
    cadence: Cadence = Cadence.DAILY
    points_per_completion: int = Field(
        default=DEFAULT_POINTS_PER_COMPLETION,
        ge=MIN_POINTS_PER_COMPLETION,
        le=MAX_POINTS_PER_COMPLETION,
    )
    is_archived: bool = False

    @field_validator("name")
    @classmethod
    def _require_non_blank_name(cls, value: str) -> str:
        """Reject names that are empty once surrounding whitespace is removed."""
        stripped = value.strip()
        if not stripped:
            raise ValueError("name must not be blank")
        return stripped

    @field_validator("description")
    @classmethod
    def _normalise_description(cls, value: str | None) -> str | None:
        """Treat a blank description as absent rather than storing whitespace."""
        if value is None:
            return None
        return value.strip() or None


class HabitCreate(HabitFields):
    """Payload for creating a habit."""


class HabitUpdate(HabitFields):
    """Payload for replacing a habit.

    This is a full replacement, so any field omitted by the client returns to
    its default rather than keeping its previous value.
    """


class Habit(HabitFields):
    """A stored habit."""

    id: int
    created_at: datetime
