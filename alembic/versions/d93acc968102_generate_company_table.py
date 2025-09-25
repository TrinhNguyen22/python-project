"""generate company table

Revision ID: d93acc968102
Revises: 
Create Date: 2025-09-22 15:36:30.245858

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd93acc968102'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'company',
        sa.Column('id', sa.UUID, primary_key=True, nullable=False),
        sa.Column('name', sa.String),
        sa.Column('description', sa.String),
        sa.Column('mode', sa.String),
        sa.Column('rating', sa.Integer)
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('fk_company_owner', 'user')
    op.drop_table('company')
