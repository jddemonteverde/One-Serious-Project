"""In-memory storage for habits.

This is deliberately temporary. PostgreSQL persistence replaces it in a later
ticket, so state here is process-local and is lost when the service restarts.
"""

from __future__ import annotations

import threading
from datetime import UTC, datetime
from itertools import count

from habit_tracker.schemas import Habit, HabitCreate, HabitUpdate


class HabitStore:
    """A thread-safe collection of habits.

    FastAPI runs synchronous endpoints in a worker threadpool, so this store can
    be reached from several threads at once. The lock keeps the identifier
    counter and the mapping consistent with each other.
    """

    def __init__(self) -> None:
        self._habits: dict[int, Habit] = {}
        self._next_id = count(1)
        self._lock = threading.Lock()

    def list(self) -> list[Habit]:
        """Return every habit, oldest first."""
        with self._lock:
            return sorted(self._habits.values(), key=lambda habit: habit.id)

    def get(self, habit_id: int) -> Habit | None:
        """Return one habit, or None when no habit has that identifier."""
        with self._lock:
            return self._habits.get(habit_id)

    def create(self, payload: HabitCreate) -> Habit:
        """Store a new habit and return it."""
        with self._lock:
            habit = Habit(
                id=next(self._next_id),
                created_at=datetime.now(UTC),
                **payload.model_dump(),
            )
            self._habits[habit.id] = habit
            return habit

    def replace(self, habit_id: int, payload: HabitUpdate) -> Habit | None:
        """Replace a habit's fields, keeping its identifier and creation time.

        Returns None when no habit has that identifier.
        """
        with self._lock:
            existing = self._habits.get(habit_id)
            if existing is None:
                return None

            replacement = Habit(
                id=existing.id,
                created_at=existing.created_at,
                **payload.model_dump(),
            )
            self._habits[habit_id] = replacement
            return replacement

    def delete(self, habit_id: int) -> bool:
        """Remove a habit. Returns False when no habit has that identifier."""
        with self._lock:
            return self._habits.pop(habit_id, None) is not None
