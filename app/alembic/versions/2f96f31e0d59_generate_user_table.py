"""generate user table

Revision ID: 2f96f31e0d59
Revises: 9e12bc7cc439
Create Date: 2025-09-23 00:18:44.956766

"""
from typing import Sequence, Union
from uuid import uuid4

from alembic import op
import sqlalchemy as sa

from settings import ADMIN_DEFAULT_PASSWORD
from schemas.user import hash_password


# revision identifiers, used by Alembic.
revision: str = '2f96f31e0d59'
down_revision: Union[str, Sequence[str], None] = '9e12bc7cc439'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    user_table = op.create_table(
        'user',
        sa.Column('id', sa.UUID, primary_key=True, nullable=False),
        sa.Column('email', sa.String, unique=True, nullable=True, index=True),
        sa.Column('username', sa.String),
        sa.Column('first_name', sa.String),
        sa.Column('last_name', sa.String),
        sa.Column('hashed_password', sa.String),
        sa.Column('is_active', sa.Boolean, default=True),
        sa.Column('is_admin', sa.Boolean, default=False)
    )
    op.create_index(
        'idx_usr_fst_lst_name',
        'user',
        ['first_name', 'last_name']
    )
    op.add_column('task', sa.Column('owner_id', sa.UUID, nullable=True))
    op.create_foreign_key(
        'fk_task_owner',
        'task',
        'user',
        ['owner_id'],
        ['id']
    )
    op.add_column('user', sa.Column('company_id', sa.UUID, nullable=True))
    op.create_foreign_key(
        'fk_company_owner',
        'user',
        'company',
        ['company_id'],
        ['id']
    )

    op.bulk_insert(user_table, [
        {
            'id': uuid4(),
            'email': 'python_fastapi@sample.com',
            'username': 'fa_admin',
            'first_name': 'FastAPI',
            'last_name': 'Admin',
            'hashed_password': hash_password(ADMIN_DEFAULT_PASSWORD),
            'is_active': True,
            'is_admin': True
        }
    ])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('fk_task_owner', 'task')
    op.drop_table('user')
