"""Habits API routes."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status

from habit_tracker.schemas import Habit, HabitCreate, HabitUpdate
from habit_tracker.storage import HabitStore

router = APIRouter(prefix="/habits", tags=["habits"])


def get_store(request: Request) -> HabitStore:
    """Return the habit store held on the application state."""
    return request.app.state.habit_store


StoreDependency = Annotated[HabitStore, Depends(get_store)]


def _not_found(habit_id: int) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Habit {habit_id} was not found.",
    )


@router.post("", response_model=Habit, status_code=status.HTTP_201_CREATED)
def create_habit(payload: HabitCreate, store: StoreDependency) -> Habit:
    """Create a habit."""
    return store.create(payload)


@router.get("", response_model=list[Habit])
def list_habits(store: StoreDependency) -> list[Habit]:
    """List every habit, oldest first."""
    return store.list()


@router.get("/{habit_id}", response_model=Habit)
def read_habit(habit_id: int, store: StoreDependency) -> Habit:
    """Return one habit."""
    habit = store.get(habit_id)
    if habit is None:
        raise _not_found(habit_id)
    return habit


@router.put("/{habit_id}", response_model=Habit)
def replace_habit(habit_id: int, payload: HabitUpdate, store: StoreDependency) -> Habit:
    """Replace a habit's fields, keeping its identifier and creation time."""
    habit = store.replace(habit_id, payload)
    if habit is None:
        raise _not_found(habit_id)
    return habit


@router.delete("/{habit_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_habit(habit_id: int, store: StoreDependency) -> None:
    """Delete a habit."""
    if not store.delete(habit_id):
        raise _not_found(habit_id)
