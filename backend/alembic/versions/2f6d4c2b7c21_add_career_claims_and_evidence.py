"""add career claims and evidence tables

Revision ID: 2f6d4c2b7c21
Revises: d42b9c8e3f11
Create Date: 2026-09-15 00:00:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "2f6d4c2b7c21"
down_revision: Union[str, None] = "d42b9c8e3f11"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "career_claims",
        sa.Column("career_profile_id", sa.UUID(), nullable=False),
        sa.Column("claim_type", sa.String(length=30), nullable=False),
        sa.Column("claim_text", sa.Text(), nullable=False),
        sa.Column("subject", sa.String(length=255), nullable=False),
        sa.Column("context", sa.Text(), nullable=True),
        sa.Column("experience_type", sa.String(length=30), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=True),
        sa.Column("end_date", sa.Date(), nullable=True),
        sa.Column("proficiency", sa.String(length=30), nullable=True),
        sa.Column("skill_name", sa.String(length=150), nullable=True),
        sa.Column("status", sa.String(length=30), nullable=False, server_default="unsupported"),
        sa.Column("confidence", sa.Numeric(precision=4, scale=2), nullable=False, server_default="0.00"),
        sa.Column("candidate_confirmed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.CheckConstraint("end_date IS NULL OR start_date IS NULL OR end_date >= start_date", name="ck_claim_dates"),
        sa.ForeignKeyConstraint(["career_profile_id"], ["career_profiles.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_career_claims_career_profile_id", "career_claims", ["career_profile_id"])

    op.create_table(
        "evidence",
        sa.Column("career_profile_id", sa.UUID(), nullable=False),
        sa.Column("source_type", sa.String(length=30), nullable=False),
        sa.Column("source_reference", sa.String(length=255), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("content_hash", sa.String(length=128), nullable=False),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["career_profile_id"], ["career_profiles.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_evidence_career_profile_id", "evidence", ["career_profile_id"])
    op.create_index("ix_evidence_content_hash", "evidence", ["content_hash"])

    op.create_table(
        "claim_evidence",
        sa.Column("claim_id", sa.UUID(), nullable=False),
        sa.Column("evidence_id", sa.UUID(), nullable=False),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["claim_id"], ["career_claims.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["evidence_id"], ["evidence.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("claim_id", "evidence_id", name="uq_claim_evidence"),
    )
    op.create_index("ix_claim_evidence_claim_id", "claim_evidence", ["claim_id"])
    op.create_index("ix_claim_evidence_evidence_id", "claim_evidence", ["evidence_id"])


def downgrade() -> None:
    op.drop_index("ix_claim_evidence_evidence_id", table_name="claim_evidence")
    op.drop_index("ix_claim_evidence_claim_id", table_name="claim_evidence")
    op.drop_table("claim_evidence")
    op.drop_index("ix_evidence_content_hash", table_name="evidence")
    op.drop_index("ix_evidence_career_profile_id", table_name="evidence")
    op.drop_table("evidence")
    op.drop_index("ix_career_claims_career_profile_id", table_name="career_claims")
    op.drop_table("career_claims")
