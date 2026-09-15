"""add private resume storage metadata

Revision ID: b11a4d8f6c20
Revises: 8c1a2f9197b5
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "b11a4d8f6c20"
down_revision: Union[str, None] = "8c1a2f9197b5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("resume_files", sa.Column("storage_key", sa.String(length=500), nullable=True))
    op.add_column("resume_files", sa.Column("checksum", sa.String(length=64), nullable=True))
    op.create_index("ix_resume_files_checksum", "resume_files", ["checksum"])


def downgrade() -> None:
    op.drop_index("ix_resume_files_checksum", table_name="resume_files")
    op.drop_column("resume_files", "checksum")
    op.drop_column("resume_files", "storage_key")