"""Add few columns to post table

Revision ID: 26247033e9cb
Revises: 05eacf58c44e
Create Date: 2026-06-17 14:57:39.583377

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '26247033e9cb'
down_revision: Union[str, Sequence[str], None] = '05eacf58c44e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("post", 
                  sa.Column('published', sa.Boolean(), nullable=False, server_default="TRUE"),)
    op.add_column('post', sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),)
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("post", "published")
    op.drop_column("post", "created_at")
    pass
