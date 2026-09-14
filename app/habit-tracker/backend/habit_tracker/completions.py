"""Habit completions API routes."""

from __future__ import annotations

from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from habit_tracker.dependencies import SessionDependency, TodayDependency
from habit_tracker.schemas import Completion, CompletionCreate
from habit_tracker.storage import (
    CompletionNotFoundError,
    CompletionRepository,
    DuplicateCompletionError,
    FutureCompletionError,
    HabitNotFoundError,
)

router = APIRouter(prefix="/habits/{habit_id}/completions", tags=["completions"])


def get_repository(
    session: SessionDependency, today: TodayDependency
) -> CompletionRepository:
    """Build the completion repository for this request."""
    return CompletionRepository(session, today)


RepositoryDependency = Annotated[CompletionRepository, Depends(get_repository)]


def _habit_not_found(habit_id: int) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Habit {habit_id} was not found.",
    )


@router.post("", response_model=Completion, status_code=status.HTTP_201_CREATED)
def log_completion(
    habit_id: int,
    repository: RepositoryDependency,
    payload: CompletionCreate | None = None,
) -> Completion:
    """Record that the habit was done on a day, today by default.

    The body may be omitted entirely, which logs today.
    """
    completed_on = None if payload is None else payload.completed_on
    try:
        return repository.log(habit_id, completed_on)
    except HabitNotFoundError:
        raise _habit_not_found(habit_id) from None
    except FutureCompletionError as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=f"completed_on {error} is in the future.",
        ) from None
    except DuplicateCompletionError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Habit {habit_id} is already completed on {error}.",
        ) from None


@router.get("", response_model=list[Completion])
def list_completions(habit_id: int, repository: RepositoryDependency) -> list[Completion]:
    """List the habit's completions, oldest first."""
    try:
        return repository.list(habit_id)
    except HabitNotFoundError:
        raise _habit_not_found(habit_id) from None


@router.delete("/{completed_on}", status_code=status.HTTP_204_NO_CONTENT)
def remove_completion(
    habit_id: int, completed_on: date, repository: RepositoryDependency
) -> None:
    """Remove the completion for a day and rebuild the habit's streaks."""
    try:
        repository.remove(habit_id, completed_on)
    except HabitNotFoundError:
        raise _habit_not_found(habit_id) from None
    except CompletionNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Habit {habit_id} has no completion on {completed_on}.",
        ) from None
