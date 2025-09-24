"""generate task table

Revision ID: 9e12bc7cc439
Revises: d93acc968102
Create Date: 2025-09-22 15:38:00.134998

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9e12bc7cc439'
down_revision: Union[str, Sequence[str], None] = 'd93acc968102'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'task',
        sa.Column('id', sa.UUID, primary_key=True, nullable=False),
        sa.Column('summary', sa.String),
        sa.Column('description', sa.String),
        sa.Column('status', sa.String),
        sa.Column('priority', sa.String)
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('task')
