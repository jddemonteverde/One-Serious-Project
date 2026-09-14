"""Request-scoped dependencies shared by the API routers."""

from __future__ import annotations

from collections.abc import Iterator
from datetime import date, datetime
from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy.orm import Session


def get_session(request: Request) -> Iterator[Session]:
    """Yield a database session scoped to one request."""
    session_factory = request.app.state.session_factory
    with session_factory() as session:
        yield session


def get_today(request: Request) -> date:
    """Return today's date in the configured time zone.

    Resolved once per request so that every decision in the request, from
    defaulting a completion date to judging a streak, agrees on what day it is.
    """
    return datetime.now(request.app.state.settings.timezone).date()


SessionDependency = Annotated[Session, Depends(get_session)]
TodayDependency = Annotated[date, Depends(get_today)]
