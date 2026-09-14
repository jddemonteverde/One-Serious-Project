"""Add habit completions and streak aggregates.

Creates the ``habit_completions`` table, unique on habit and day, and adds the
maintained streak columns to ``habits``. Existing habits start with no streak
and no last completion, which is correct because they have no completions.

Revision ID: ab42ae023b72
Revises: cc99e69d68d3
Create Date: 2026-09-14 19:45:20.568414
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "ab42ae023b72"
down_revision: str | Sequence[str] | None = "cc99e69d68d3"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "habit_completions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("habit_id", sa.Integer(), nullable=False),
        sa.Column("completed_on", sa.Date(), nullable=False),
        sa.Column("points_awarded", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["habit_id"], ["habits.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "habit_id", "completed_on", name="uq_habit_completions_habit_day"
        ),
    )
    op.create_index(
        op.f("ix_habit_completions_habit_id"),
        "habit_completions",
        ["habit_id"],
        unique=False,
    )
    op.add_column(
        "habits",
        sa.Column("current_streak", sa.Integer(), server_default="0", nullable=False),
    )
    op.add_column(
        "habits",
        sa.Column("longest_streak", sa.Integer(), server_default="0", nullable=False),
    )
    op.add_column("habits", sa.Column("last_completed_on", sa.Date(), nullable=True))


def downgrade() -> None:
    op.drop_column("habits", "last_completed_on")
    op.drop_column("habits", "longest_streak")
    op.drop_column("habits", "current_streak")
    op.drop_index(op.f("ix_habit_completions_habit_id"), table_name="habit_completions")
    op.drop_table("habit_completions")
