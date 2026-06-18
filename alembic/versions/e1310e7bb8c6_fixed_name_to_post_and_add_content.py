"""Fixed name to post and add content

Revision ID: e1310e7bb8c6
Revises: 44ce9fed2c92
Create Date: 2026-06-17 06:29:36.556689

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e1310e7bb8c6'
down_revision: Union[str, Sequence[str], None] = '44ce9fed2c92'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("post", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("post", "content")
    pass
