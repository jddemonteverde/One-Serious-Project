"""Habits API routes."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from habit_tracker.schemas import Habit, HabitCreate, HabitUpdate
from habit_tracker.storage import HabitRepository

router = APIRouter(prefix="/habits", tags=["habits"])


def get_session(request: Request) -> Iterator[Session]:
    """Yield a database session scoped to one request."""
    session_factory = request.app.state.session_factory
    with session_factory() as session:
        yield session


SessionDependency = Annotated[Session, Depends(get_session)]


def get_repository(session: SessionDependency) -> HabitRepository:
    """Build the habit repository for this request."""
    return HabitRepository(session)


RepositoryDependency = Annotated[HabitRepository, Depends(get_repository)]


def _not_found(habit_id: int) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Habit {habit_id} was not found.",
    )


@router.post("", response_model=Habit, status_code=status.HTTP_201_CREATED)
def create_habit(payload: HabitCreate, repository: RepositoryDependency) -> Habit:
    """Create a habit."""
    return repository.create(payload)


@router.get("", response_model=list[Habit])
def list_habits(repository: RepositoryDependency) -> list[Habit]:
    """List every habit, oldest first."""
    return repository.list()


@router.get("/{habit_id}", response_model=Habit)
def read_habit(habit_id: int, repository: RepositoryDependency) -> Habit:
    """Return one habit."""
    habit = repository.get(habit_id)
    if habit is None:
        raise _not_found(habit_id)
    return habit


@router.put("/{habit_id}", response_model=Habit)
def replace_habit(habit_id: int, payload: HabitUpdate, repository: RepositoryDependency) -> Habit:
    """Replace a habit's fields, keeping its identifier and creation time."""
    habit = repository.replace(habit_id, payload)
    if habit is None:
        raise _not_found(habit_id)
    return habit


@router.delete("/{habit_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_habit(habit_id: int, repository: RepositoryDependency) -> None:
    """Delete a habit."""
    if not repository.delete(habit_id):
        raise _not_found(habit_id)
