"""add resume files and proposals

Revision ID: 8c1a2f9197b5
Revises: 2f6d4c2b7c21
Create Date: 2026-09-15 00:00:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "8c1a2f9197b5"
down_revision: Union[str, None] = "2f6d4c2b7c21"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "resume_files",
        sa.Column("career_profile_id", sa.UUID(), nullable=False),
        sa.Column("filename", sa.String(length=255), nullable=False),
        sa.Column("content_type", sa.String(length=100), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("file_size", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("status", sa.String(length=30), nullable=False, server_default="uploaded"),
        sa.Column("extracted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["career_profile_id"], ["career_profiles.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_resume_files_career_profile_id", "resume_files", ["career_profile_id"])

    op.create_table(
        "resume_proposals",
        sa.Column("resume_file_id", sa.UUID(), nullable=False),
        sa.Column("proposal_type", sa.String(length=30), nullable=False),
        sa.Column("field_name", sa.String(length=100), nullable=False),
        sa.Column("proposed_value", sa.Text(), nullable=False),
        sa.Column("source_excerpt", sa.Text(), nullable=True),
        sa.Column("confidence", sa.Numeric(precision=4, scale=2), nullable=False, server_default="0.00"),
        sa.Column("decision", sa.String(length=30), nullable=False, server_default="pending"),
        sa.Column("review_notes", sa.Text(), nullable=True),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["resume_file_id"], ["resume_files.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_resume_proposals_resume_file_id", "resume_proposals", ["resume_file_id"])


def downgrade() -> None:
    op.drop_index("ix_resume_proposals_resume_file_id", table_name="resume_proposals")
    op.drop_table("resume_proposals")
    op.drop_index("ix_resume_files_career_profile_id", table_name="resume_files")
    op.drop_table("resume_files")
