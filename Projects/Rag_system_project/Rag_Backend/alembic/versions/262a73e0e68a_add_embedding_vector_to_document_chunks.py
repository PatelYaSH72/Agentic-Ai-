"""add embedding vector to document chunks

Revision ID: 262a73e0e68a
Revises: 1fa8f3c1e254
Create Date: 2026-08-08 21:25:13.783366

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from pgvector.sqlalchemy import Vector


# revision identifiers, used by Alembic.
revision: str = "262a73e0e68a"

down_revision: Union[str, Sequence[str], None] = "1fa8f3c1e254"

branch_labels: Union[str, Sequence[str], None] = None

depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        "document_chunks",
        sa.Column(
            "embedding",
            Vector(384),
            nullable=True,
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column(
        "document_chunks",
        "embedding",
    )