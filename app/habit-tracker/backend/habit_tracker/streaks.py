"""Streak arithmetic derived from completion dates.

A streak is a run of consecutive periods, each containing at least one
completion. For a daily habit the period is the calendar day; for a weekly
habit it is the ISO week, so completing a weekly habit on any day of the week
counts for that week.

The current streak is the run ending at the most recent completion, and it is
only alive while that completion falls in the current period or the one just
before it: the current period is not missed until it is over. A streak that
was alive when it was stored can therefore have lapsed by the time it is read,
which :func:`current_streak` accounts for.

These functions are pure so that streaks can be recomputed from completion
records alone, which is what keeps the stored aggregates recoverable.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from datetime import date, timedelta

from habit_tracker.schemas import Cadence

_PERIOD_LENGTH = {
    Cadence.DAILY: timedelta(days=1),
    Cadence.WEEKLY: timedelta(days=7),
}


@dataclass(frozen=True)
class Streaks:
    """Streak counters for one habit."""

    current: int
    longest: int


def period_start(day: date, cadence: Cadence) -> date:
    """Return the first day of the period containing ``day``."""
    if cadence is Cadence.WEEKLY:
        return day - timedelta(days=day.weekday())
    return day


def compute_streaks(
    completed_on: Iterable[date], cadence: Cadence, today: date
) -> Streaks:
    """Derive both streak counters from a habit's completion dates."""
    step = _PERIOD_LENGTH[cadence]
    periods = sorted({period_start(day, cadence) for day in completed_on})

    longest = 0
    run = 0
    previous: date | None = None
    for period in periods:
        run = run + 1 if previous is not None and period - previous == step else 1
        longest = max(longest, run)
        previous = period

    if previous is None:
        return Streaks(current=0, longest=0)

    current = run if _is_alive(previous, cadence, today) else 0
    return Streaks(current=current, longest=longest)


def current_streak(
    stored: int, last_completed_on: date | None, cadence: Cadence, today: date
) -> int:
    """Return the stored current streak, or zero if it has lapsed since storing.

    The stored value was correct on the day of the last completion change.
    Reading it later must still reset it once a period has been missed.
    """
    if last_completed_on is None or not _is_alive(last_completed_on, cadence, today):
        return 0
    return stored


def _is_alive(last_completed_on: date, cadence: Cadence, today: date) -> bool:
    """Whether a streak ending at ``last_completed_on`` is still unbroken."""
    last_period = period_start(last_completed_on, cadence)
    current_period = period_start(today, cadence)
    return last_period in (current_period, current_period - _PERIOD_LENGTH[cadence])
