"""add structured career profile tables

Revision ID: c31a8d7f2e10
Revises: fa9ac77da9fd
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "c31a8d7f2e10"
down_revision: Union[str, None] = "fa9ac77da9fd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "experiences",
        sa.Column("company_name", sa.String(length=255), nullable=False),
        sa.Column("job_title", sa.String(length=255), nullable=False),
        sa.Column("location", sa.String(length=150), nullable=True),
        sa.Column("employment_type", sa.String(length=30), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=True),
        sa.Column("is_current", sa.Boolean(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("career_profile_id", sa.UUID(), nullable=False),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.CheckConstraint("end_date IS NULL OR end_date >= start_date", name="ck_experience_dates"),
        sa.CheckConstraint("NOT is_current OR end_date IS NULL", name="ck_current_experience_end_date"),
        sa.ForeignKeyConstraint(["career_profile_id"], ["career_profiles.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_experiences_career_profile_id", "experiences", ["career_profile_id"])

    op.create_table(
        "projects",
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("role", sa.String(length=255), nullable=True),
        sa.Column("project_type", sa.String(length=30), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=True),
        sa.Column("end_date", sa.Date(), nullable=True),
        sa.Column("repository_url", sa.String(length=500), nullable=True),
        sa.Column("project_url", sa.String(length=500), nullable=True),
        sa.Column("career_profile_id", sa.UUID(), nullable=False),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.CheckConstraint("end_date IS NULL OR start_date IS NULL OR end_date >= start_date", name="ck_project_dates"),
        sa.ForeignKeyConstraint(["career_profile_id"], ["career_profiles.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_projects_career_profile_id", "projects", ["career_profile_id"])

    op.create_table(
        "education",
        sa.Column("institution", sa.String(length=255), nullable=False),
        sa.Column("degree", sa.String(length=255), nullable=False),
        sa.Column("field_of_study", sa.String(length=255), nullable=True),
        sa.Column("start_date", sa.Date(), nullable=True),
        sa.Column("end_date", sa.Date(), nullable=True),
        sa.Column("grade", sa.String(length=100), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("career_profile_id", sa.UUID(), nullable=False),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.CheckConstraint("end_date IS NULL OR start_date IS NULL OR end_date >= start_date", name="ck_education_dates"),
        sa.ForeignKeyConstraint(["career_profile_id"], ["career_profiles.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_education_career_profile_id", "education", ["career_profile_id"])

    op.create_table(
        "certifications",
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("issuing_organization", sa.String(length=255), nullable=False),
        sa.Column("issue_date", sa.Date(), nullable=True),
        sa.Column("expiry_date", sa.Date(), nullable=True),
        sa.Column("credential_id", sa.String(length=255), nullable=True),
        sa.Column("credential_url", sa.String(length=500), nullable=True),
        sa.Column("career_profile_id", sa.UUID(), nullable=False),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.CheckConstraint("expiry_date IS NULL OR issue_date IS NULL OR expiry_date >= issue_date", name="ck_certification_dates"),
        sa.ForeignKeyConstraint(["career_profile_id"], ["career_profiles.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_certifications_career_profile_id", "certifications", ["career_profile_id"])

    op.create_table(
        "skills",
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.Column("normalized_name", sa.String(length=150), nullable=False),
        sa.Column("category", sa.String(length=100), nullable=True),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("normalized_name"),
    )
    op.create_index("ix_skills_normalized_name", "skills", ["normalized_name"])

    op.create_table(
        "candidate_skills",
        sa.Column("career_profile_id", sa.UUID(), nullable=False),
        sa.Column("skill_id", sa.UUID(), nullable=False),
        sa.Column("experience_type", sa.String(length=30), nullable=False),
        sa.Column("proficiency", sa.String(length=30), nullable=True),
        sa.Column("years_used", sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column("first_used", sa.Date(), nullable=True),
        sa.Column("last_used", sa.Date(), nullable=True),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.CheckConstraint("last_used IS NULL OR first_used IS NULL OR last_used >= first_used", name="ck_candidate_skill_dates"),
        sa.ForeignKeyConstraint(["career_profile_id"], ["career_profiles.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["skill_id"], ["skills.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("career_profile_id", "skill_id", name="uq_candidate_skill_profile_skill"),
    )
    op.create_index("ix_candidate_skills_career_profile_id", "candidate_skills", ["career_profile_id"])
    op.create_index("ix_candidate_skills_skill_id", "candidate_skills", ["skill_id"])


def downgrade() -> None:
    op.drop_table("candidate_skills")
    op.drop_table("skills")
    op.drop_table("certifications")
    op.drop_table("education")
    op.drop_table("projects")
    op.drop_table("experiences")