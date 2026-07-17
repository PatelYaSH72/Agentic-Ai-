"""Initial migration

Revision ID: bd7d2368e9f3
Revises: d475abd91dde
Create Date: 2026-07-18 00:18:34.952207

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bd7d2368e9f3'
down_revision: Union[str, Sequence[str], None] = 'd475abd91dde'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
