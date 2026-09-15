"""create candidate job matches

Revision ID: d53f8a2c1e40
Revises: c42e7b1a9d30
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "d53f8a2c1e40"
down_revision: Union[str, None] = "c42e7b1a9d30"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "candidate_job_matches",
        sa.Column("career_profile_id", sa.UUID(), nullable=False),
        sa.Column("job_id", sa.UUID(), nullable=False),
        sa.Column("algorithm_version", sa.String(length=50), nullable=False, server_default="matching-v1"),
        sa.Column("overall_score", sa.Numeric(precision=5, scale=2), nullable=False),
        sa.Column("profile_coverage", sa.Numeric(precision=5, scale=2), nullable=False),
        sa.Column("required_score", sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column("preferred_score", sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column("analysis_status", sa.String(length=30), nullable=False),
        sa.Column("critical_gaps", sa.JSON(), nullable=False),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["career_profile_id"], ["career_profiles.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["job_id"], ["jobs.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_candidate_job_matches_career_profile_id", "candidate_job_matches", ["career_profile_id"])
    op.create_index("ix_candidate_job_matches_job_id", "candidate_job_matches", ["job_id"])
    op.create_table(
        "match_details",
        sa.Column("match_id", sa.UUID(), nullable=False),
        sa.Column("job_requirement_id", sa.UUID(), nullable=False),
        sa.Column("career_claim_id", sa.UUID(), nullable=True),
        sa.Column("match_type", sa.String(length=30), nullable=False),
        sa.Column("score", sa.Numeric(precision=5, scale=2), nullable=False),
        sa.Column("explanation", sa.Text(), nullable=False),
        sa.Column("gap_category", sa.String(length=40), nullable=True),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["match_id"], ["candidate_job_matches.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["job_requirement_id"], ["job_requirements.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["career_claim_id"], ["career_claims.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_match_details_match_id", "match_details", ["match_id"])
    op.create_index("ix_match_details_job_requirement_id", "match_details", ["job_requirement_id"])


def downgrade() -> None:
    op.drop_index("ix_match_details_job_requirement_id", table_name="match_details")
    op.drop_index("ix_match_details_match_id", table_name="match_details")
    op.drop_table("match_details")
    op.drop_index("ix_candidate_job_matches_job_id", table_name="candidate_job_matches")
    op.drop_index("ix_candidate_job_matches_career_profile_id", table_name="candidate_job_matches")
    op.drop_table("candidate_job_matches")