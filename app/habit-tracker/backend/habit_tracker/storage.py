"""Habit persistence backed by PostgreSQL.

The repository returns Pydantic schemas rather than ORM instances so that the
routes and response models are unaffected by how habits are stored.
"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from habit_tracker import models
from habit_tracker.database import get_default_user
from habit_tracker.schemas import Habit, HabitCreate, HabitUpdate


def _to_schema(record: models.Habit) -> Habit:
    return Habit.model_validate(
        {
            "id": record.id,
            "name": record.name,
            "description": record.description,
            "cadence": record.cadence,
            "points_per_completion": record.points_per_completion,
            "is_archived": record.is_archived,
            "created_at": record.created_at,
        }
    )


class HabitRepository:
    """Reads and writes habits for the current user.

    One instance is built per request and commits its own writes, so a failed
    request leaves nothing partially applied.
    """

    def __init__(self, session: Session) -> None:
        self._session = session
        self._owner = get_default_user(session)

    def _select_owned(self) -> select:
        return select(models.Habit).where(models.Habit.user_id == self._owner.id)

    def _find(self, habit_id: int) -> models.Habit | None:
        return self._session.scalars(
            self._select_owned().where(models.Habit.id == habit_id)
        ).first()

    def list(self) -> list[Habit]:
        """Return every habit, oldest first."""
        records = self._session.scalars(
            self._select_owned().order_by(models.Habit.id)
        ).all()
        return [_to_schema(record) for record in records]

    def get(self, habit_id: int) -> Habit | None:
        """Return one habit, or None when no habit has that identifier."""
        record = self._find(habit_id)
        return None if record is None else _to_schema(record)

    def create(self, payload: HabitCreate) -> Habit:
        """Store a new habit and return it."""
        record = models.Habit(
            user_id=self._owner.id,
            name=payload.name,
            description=payload.description,
            cadence=payload.cadence.value,
            points_per_completion=payload.points_per_completion,
            is_archived=payload.is_archived,
        )
        self._session.add(record)
        self._session.commit()
        self._session.refresh(record)
        return _to_schema(record)

    def replace(self, habit_id: int, payload: HabitUpdate) -> Habit | None:
        """Replace a habit's fields, keeping its identifier and creation time.

        Returns None when no habit has that identifier.
        """
        record = self._find(habit_id)
        if record is None:
            return None

        record.name = payload.name
        record.description = payload.description
        record.cadence = payload.cadence.value
        record.points_per_completion = payload.points_per_completion
        record.is_archived = payload.is_archived
        self._session.commit()
        self._session.refresh(record)
        return _to_schema(record)

    def delete(self, habit_id: int) -> bool:
        """Remove a habit. Returns False when no habit has that identifier."""
        record = self._find(habit_id)
        if record is None:
            return False

        self._session.delete(record)
        self._session.commit()
        return True
