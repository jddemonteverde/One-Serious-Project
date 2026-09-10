"""Database engine, session lifecycle, and development-time schema creation."""

from __future__ import annotations

import logging

from sqlalchemy import Engine, create_engine, select
from sqlalchemy.engine import URL
from sqlalchemy.exc import OperationalError, SQLAlchemyError
from sqlalchemy.orm import Session, sessionmaker

from habit_tracker.config import Settings
from habit_tracker.models import Base, User

DEFAULT_USER_DISPLAY_NAME = "Local User"

logger = logging.getLogger(__name__)


def build_database_url(settings: Settings) -> URL:
    """Build the connection URL.

    ``URL`` masks the password in its string form, but treat the object as a
    secret regardless and never interpolate it into a log message.
    """
    return URL.create(
        "postgresql+psycopg",
        username=settings.db_user,
        password=settings.db_password or None,
        host=settings.db_host,
        port=settings.db_port,
        database=settings.db_name,
    )


def create_database_engine(settings: Settings) -> Engine:
    """Create the engine.

    ``pool_pre_ping`` checks a pooled connection before handing it out, so the
    service recovers on its own after the database restarts instead of serving
    errors from stale connections.
    """
    return create_engine(build_database_url(settings), pool_pre_ping=True)


def create_session_factory(engine: Engine) -> sessionmaker[Session]:
    """Create the session factory used for each request."""
    return sessionmaker(bind=engine, expire_on_commit=False)


def prepare_database(engine: Engine, settings: Settings) -> bool:
    """Create tables and seed the default user, reporting whether it worked.

    Creating the schema here is temporary. Alembic migrations replace it in the
    next ticket, at which point this function should only verify connectivity.

    A failure is logged and reported rather than raised: the service must still
    start when the database is down, so that liveness and readiness can be told
    apart once health endpoints exist.
    """
    try:
        Base.metadata.create_all(engine)
        with Session(engine) as session, session.begin():
            get_default_user(session)
    except OperationalError:
        logger.error(
            "Database unreachable at %s:%s/%s. The service will start, but "
            "requests that need the database will fail until it is reachable.",
            settings.db_host,
            settings.db_port,
            settings.db_name,
        )
        return False
    except SQLAlchemyError as error:
        # Reached the database but could not prepare it: a schema or permission
        # problem, which needs a different fix from an outage.
        logger.error(
            "Database reachable at %s:%s/%s but preparation failed (%s). "
            "This is a schema or permission problem, not an outage.",
            settings.db_host,
            settings.db_port,
            settings.db_name,
            type(error).__name__,
        )
        return False

    logger.info(
        "Database ready at %s:%s/%s",
        settings.db_host,
        settings.db_port,
        settings.db_name,
    )
    return True


def get_default_user(session: Session) -> User:
    """Return the seeded user, creating it when the table is empty.

    Authentication arrives in a later milestone. Until then every habit belongs
    to this single user. Resolving it per request keeps the service self-healing
    if the database is reset while it is running.
    """
    user = session.scalars(select(User).order_by(User.id).limit(1)).first()
    if user is None:
        user = User(display_name=DEFAULT_USER_DISPLAY_NAME)
        session.add(user)
        session.flush()
    return user
