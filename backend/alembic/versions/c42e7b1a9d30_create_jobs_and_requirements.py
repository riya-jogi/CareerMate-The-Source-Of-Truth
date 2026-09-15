"""create jobs and job requirements

Revision ID: c42e7b1a9d30
Revises: b11a4d8f6c20
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "c42e7b1a9d30"
down_revision: Union[str, None] = "b11a4d8f6c20"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "jobs",
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=True),
        sa.Column("company_name", sa.String(length=255), nullable=True),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("location", sa.String(length=150), nullable=True),
        sa.Column("source", sa.String(length=50), nullable=False, server_default="manual"),
        sa.Column("analysis_status", sa.String(length=30), nullable=False, server_default="pending"),
        sa.Column("analysis_error", sa.Text(), nullable=True),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_jobs_user_id", "jobs", ["user_id"])
    op.create_table(
        "job_requirements",
        sa.Column("job_id", sa.UUID(), nullable=False),
        sa.Column("requirement_text", sa.Text(), nullable=False),
        sa.Column("requirement_type", sa.String(length=30), nullable=False, server_default="skill"),
        sa.Column("importance", sa.String(length=30), nullable=False, server_default="required"),
        sa.Column("skill_name", sa.String(length=150), nullable=True),
        sa.Column("minimum_years", sa.Integer(), nullable=True),
        sa.Column("experience_type", sa.String(length=30), nullable=True),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["job_id"], ["jobs.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_job_requirements_job_id", "job_requirements", ["job_id"])


def downgrade() -> None:
    op.drop_index("ix_job_requirements_job_id", table_name="job_requirements")
    op.drop_table("job_requirements")
    op.drop_index("ix_jobs_user_id", table_name="jobs")
    op.drop_table("jobs")