"""create immutable resume versions and approvals

Revision ID: e64c9a1b7d52
Revises: d53f8a2c1e40
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "e64c9a1b7d52"
down_revision: Union[str, None] = "d53f8a2c1e40"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "resumes",
        sa.Column("career_profile_id", sa.UUID(), nullable=False),
        sa.Column("original_file_id", sa.UUID(), nullable=True),
        sa.Column("name", sa.String(length=255), nullable=False, server_default="Master Resume"),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["career_profile_id"], ["career_profiles.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["original_file_id"], ["resume_files.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_resumes_career_profile_id", "resumes", ["career_profile_id"])
    op.create_table(
        "resume_versions",
        sa.Column("resume_id", sa.UUID(), nullable=False),
        sa.Column("job_id", sa.UUID(), nullable=True),
        sa.Column("version_number", sa.Integer(), nullable=False),
        sa.Column("content_snapshot", sa.JSON(), nullable=False),
        sa.Column("template", sa.String(length=50), nullable=False, server_default="professional_ats"),
        sa.Column("status", sa.String(length=30), nullable=False, server_default="pending_review"),
        sa.Column("validation_status", sa.String(length=30), nullable=False, server_default="pass"),
        sa.Column("pdf_key", sa.String(length=500), nullable=True),
        sa.Column("docx_key", sa.String(length=500), nullable=True),
        sa.Column("pdf_checksum", sa.String(length=64), nullable=True),
        sa.Column("docx_checksum", sa.String(length=64), nullable=True),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["resume_id"], ["resumes.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["job_id"], ["jobs.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_resume_versions_resume_id", "resume_versions", ["resume_id"])
    op.create_index("ix_resume_versions_job_id", "resume_versions", ["job_id"])
    op.create_table(
        "resume_changes",
        sa.Column("resume_version_id", sa.UUID(), nullable=False),
        sa.Column("change_type", sa.String(length=30), nullable=False),
        sa.Column("section", sa.String(length=50), nullable=False),
        sa.Column("original_content", sa.Text(), nullable=True),
        sa.Column("proposed_content", sa.Text(), nullable=False),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column("risk_level", sa.String(length=20), nullable=False, server_default="low"),
        sa.Column("validation_status", sa.String(length=30), nullable=False),
        sa.Column("primary_claim_id", sa.UUID(), nullable=True),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["resume_version_id"], ["resume_versions.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["primary_claim_id"], ["career_claims.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_resume_changes_resume_version_id", "resume_changes", ["resume_version_id"])
    op.create_table(
        "approvals",
        sa.Column("resume_change_id", sa.UUID(), nullable=False),
        sa.Column("decision", sa.String(length=30), nullable=False),
        sa.Column("edited_text", sa.Text(), nullable=True),
        sa.Column("candidate_comment", sa.Text(), nullable=True),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["resume_change_id"], ["resume_changes.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("resume_change_id"),
    )


def downgrade() -> None:
    op.drop_table("approvals")
    op.drop_index("ix_resume_changes_resume_version_id", table_name="resume_changes")
    op.drop_table("resume_changes")
    op.drop_index("ix_resume_versions_job_id", table_name="resume_versions")
    op.drop_index("ix_resume_versions_resume_id", table_name="resume_versions")
    op.drop_table("resume_versions")
    op.drop_index("ix_resumes_career_profile_id", table_name="resumes")
    op.drop_table("resumes")