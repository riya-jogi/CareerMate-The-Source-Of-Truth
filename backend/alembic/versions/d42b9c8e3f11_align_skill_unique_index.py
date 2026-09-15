"""align skill unique index with model metadata

Revision ID: d42b9c8e3f11
Revises: c31a8d7f2e10
"""
from typing import Sequence, Union

from alembic import op


revision: str = "d42b9c8e3f11"
down_revision: Union[str, None] = "c31a8d7f2e10"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_index("ix_skills_normalized_name", table_name="skills")


def downgrade() -> None:
    op.create_index("ix_skills_normalized_name", "skills", ["normalized_name"])