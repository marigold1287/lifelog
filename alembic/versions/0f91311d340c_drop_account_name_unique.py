"""drop account name unique

Revision ID: 0f91311d340c
Revises: 080d91ca5958
Create Date: 2026-09-30 14:13:36.047589

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0f91311d340c'
down_revision: Union[str, Sequence[str], None] = '080d91ca5958'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.drop_constraint('account_name_key', 'account', type_='unique')


def downgrade() -> None:
    op.create_unique_constraint('account_name_key', 'account', ['name'])