"""Habit and completion persistence backed by PostgreSQL.

The repositories return Pydantic schemas rather than ORM instances so that the
routes and response models are unaffected by how records are stored.

Streaks are stored on the habit and rebuilt from its completions after every
completion change, so they never drift from the records that define them.
"""

from __future__ import annotations

from datetime import date

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from habit_tracker import models
from habit_tracker.database import get_default_user
from habit_tracker.schemas import (
    Cadence,
    Completion,
    Habit,
    HabitCreate,
    HabitUpdate,
)
from habit_tracker.streaks import compute_streaks, current_streak


class HabitNotFoundError(LookupError):
    """No habit with that identifier belongs to the current user."""


class DuplicateCompletionError(ValueError):
    """The habit is already completed on that day."""


class FutureCompletionError(ValueError):
    """The completion date is after today."""


class CompletionNotFoundError(LookupError):
    """The habit has no completion on that day."""


def _habit_to_schema(record: models.Habit, today: date) -> Habit:
    cadence = Cadence(record.cadence)
    return Habit.model_validate(
        {
            "id": record.id,
            "name": record.name,
            "description": record.description,
            "cadence": cadence,
            "points_per_completion": record.points_per_completion,
            "is_archived": record.is_archived,
            # The stored value was right when last written; it may have lapsed
            # since, and a lapsed streak must read as zero.
            "current_streak": current_streak(
                record.current_streak, record.last_completed_on, cadence, today
            ),
            "longest_streak": record.longest_streak,
            "created_at": record.created_at,
        }
    )


def _completion_to_schema(record: models.HabitCompletion) -> Completion:
    return Completion.model_validate(
        {
            "habit_id": record.habit_id,
            "completed_on": record.completed_on,
            "points_awarded": record.points_awarded,
            "created_at": record.created_at,
        }
    )


def _find_owned_habit(
    session: Session, owner_id: int, habit_id: int
) -> models.Habit | None:
    return session.scalars(
        select(models.Habit)
        .where(models.Habit.user_id == owner_id)
        .where(models.Habit.id == habit_id)
    ).first()


def _refresh_streaks(session: Session, habit: models.Habit, today: date) -> None:
    """Rebuild the habit's streak aggregates from its completion records."""
    dates = session.scalars(
        select(models.HabitCompletion.completed_on).where(
            models.HabitCompletion.habit_id == habit.id
        )
    ).all()
    streaks = compute_streaks(dates, Cadence(habit.cadence), today)
    habit.current_streak = streaks.current
    habit.longest_streak = streaks.longest
    habit.last_completed_on = max(dates, default=None)


class HabitRepository:
    """Reads and writes habits for the current user.

    One instance is built per request and commits its own writes, so a failed
    request leaves nothing partially applied. ``today`` is the current date in
    the configured time zone; streaks are judged against it.
    """

    def __init__(self, session: Session, today: date) -> None:
        self._session = session
        self._today = today
        self._owner = get_default_user(session)

    def _find(self, habit_id: int) -> models.Habit | None:
        return _find_owned_habit(self._session, self._owner.id, habit_id)

    def list(self) -> list[Habit]:
        """Return every habit, oldest first."""
        records = self._session.scalars(
            select(models.Habit)
            .where(models.Habit.user_id == self._owner.id)
            .order_by(models.Habit.id)
        ).all()
        return [_habit_to_schema(record, self._today) for record in records]

    def get(self, habit_id: int) -> Habit | None:
        """Return one habit, or None when no habit has that identifier."""
        record = self._find(habit_id)
        return None if record is None else _habit_to_schema(record, self._today)

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
        return _habit_to_schema(record, self._today)

    def replace(self, habit_id: int, payload: HabitUpdate) -> Habit | None:
        """Replace a habit's fields, keeping its identifier and creation time.

        Streaks are not client-editable. They are rebuilt only if the cadence
        changes, because a daily streak and a weekly streak are counted over
        different periods. Returns None when no habit has that identifier.
        """
        record = self._find(habit_id)
        if record is None:
            return None

        cadence_changed = record.cadence != payload.cadence.value
        record.name = payload.name
        record.description = payload.description
        record.cadence = payload.cadence.value
        record.points_per_completion = payload.points_per_completion
        record.is_archived = payload.is_archived
        if cadence_changed:
            _refresh_streaks(self._session, record, self._today)
        self._session.commit()
        self._session.refresh(record)
        return _habit_to_schema(record, self._today)

    def delete(self, habit_id: int) -> bool:
        """Remove a habit and its completions. Returns False when not found."""
        record = self._find(habit_id)
        if record is None:
            return False

        self._session.delete(record)
        self._session.commit()
        return True


class CompletionRepository:
    """Logs and removes completions for the current user's habits.

    Every write ends by rebuilding the habit's streaks in the same transaction,
    so the aggregates and the completion records are never committed apart.
    """

    def __init__(self, session: Session, today: date) -> None:
        self._session = session
        self._today = today
        self._owner = get_default_user(session)

    def _require_habit(self, habit_id: int) -> models.Habit:
        habit = _find_owned_habit(self._session, self._owner.id, habit_id)
        if habit is None:
            raise HabitNotFoundError(habit_id)
        return habit

    def list(self, habit_id: int) -> list[Completion]:
        """Return a habit's completions, oldest first."""
        self._require_habit(habit_id)
        records = self._session.scalars(
            select(models.HabitCompletion)
            .where(models.HabitCompletion.habit_id == habit_id)
            .order_by(models.HabitCompletion.completed_on)
        ).all()
        return [_completion_to_schema(record) for record in records]

    def log(self, habit_id: int, completed_on: date | None) -> Completion:
        """Record that the habit was done on ``completed_on``, or today.

        The points awarded are copied from the habit as it is now. The
        database's unique constraint is what detects a duplicate, so two
        concurrent requests for the same day cannot both succeed.
        """
        habit = self._require_habit(habit_id)
        day = self._today if completed_on is None else completed_on
        if day > self._today:
            raise FutureCompletionError(day)

        record = models.HabitCompletion(
            habit_id=habit.id,
            completed_on=day,
            points_awarded=habit.points_per_completion,
        )
        self._session.add(record)
        try:
            self._session.flush()
        except IntegrityError:
            self._session.rollback()
            raise DuplicateCompletionError(day) from None

        _refresh_streaks(self._session, habit, self._today)
        self._session.commit()
        self._session.refresh(record)
        return _completion_to_schema(record)

    def remove(self, habit_id: int, completed_on: date) -> None:
        """Delete the completion for that day and rebuild the streaks."""
        habit = self._require_habit(habit_id)
        record = self._session.scalars(
            select(models.HabitCompletion)
            .where(models.HabitCompletion.habit_id == habit.id)
            .where(models.HabitCompletion.completed_on == completed_on)
        ).first()
        if record is None:
            raise CompletionNotFoundError(completed_on)

        self._session.delete(record)
        self._session.flush()
        _refresh_streaks(self._session, habit, self._today)
        self._session.commit()
