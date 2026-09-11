"""Alembic environment: connects using the service's own settings.

The database URL is built from the DB_* environment variables through
``habit_tracker.config`` rather than read from ``alembic.ini``, so migrations
and the running service always target the same database with the same
credentials, and no credential is ever committed.
"""

from __future__ import annotations

from logging.config import fileConfig

from alembic import context
from sqlalchemy import create_engine, pool

from habit_tracker.config import load_settings
from habit_tracker.database import build_database_url
from habit_tracker.models import Base

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Autogenerate compares this metadata with the live schema.
target_metadata = Base.metadata

database_url = build_database_url(load_settings())


def run_migrations_offline() -> None:
    """Emit the migration SQL to stdout without connecting to a database."""
    context.configure(
        url=database_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Apply migrations over a live connection.

    ``NullPool`` because this is a short-lived process that needs exactly one
    connection; there is nothing to pool.
    """
    engine = create_engine(database_url, poolclass=pool.NullPool)

    with engine.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
