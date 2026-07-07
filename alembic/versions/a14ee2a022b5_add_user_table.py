"""add user table

Revision ID: a14ee2a022b5
Revises: e1310e7bb8c6
Create Date: 2026-06-17 06:39:14.536253

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a14ee2a022b5'
down_revision: Union[str, Sequence[str], None] = '44ce9fed2c92'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table("users",
                    sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
                    sa.Column("email", sa.String(), nullable=False),
                    sa.Column("password", sa.String(), nullable=False),
                    sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
                    sa.PrimaryKeyConstraint("id"),
                    sa.UniqueConstraint("email")
                    )
                    
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")
    pass
