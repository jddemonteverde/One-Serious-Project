"""Create the users and habits tables.

This is the initial schema. It reproduces exactly what
``Base.metadata.create_all`` produced before migrations existed, so a database
created that way can adopt this revision with ``alembic stamp head`` rather than
being rebuilt.

Revision ID: cc99e69d68d3
Revises:
Create Date: 2026-09-11 13:46:52.392662
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "cc99e69d68d3"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("display_name", sa.String(length=100), nullable=False),
        sa.Column("total_points", sa.Integer(), server_default="0", nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "habits",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("description", sa.String(length=500), nullable=True),
        sa.Column("cadence", sa.String(length=16), nullable=False),
        sa.Column("points_per_completion", sa.Integer(), nullable=False),
        sa.Column("is_archived", sa.Boolean(), server_default="false", nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_habits_user_id"), "habits", ["user_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_habits_user_id"), table_name="habits")
    op.drop_table("habits")
    op.drop_table("users")
