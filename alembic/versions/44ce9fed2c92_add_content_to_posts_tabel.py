"""Add content to posts tabel

Revision ID: 44ce9fed2c92
Revises: c934e0f34739
Create Date: 2026-06-17 06:16:10.172398

""" 
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '44ce9fed2c92'
down_revision: Union[str, Sequence[str], None] = 'c934e0f34739'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("post", sa.Column("content", sa.String(), nullabel=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("post", "content")
    pass
