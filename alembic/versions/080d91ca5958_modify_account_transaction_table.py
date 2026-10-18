"""modify account, transaction table

Revision ID: 080d91ca5958
Revises: 482db97547fb
Create Date: 2026-09-30 14:08:51.867043

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '080d91ca5958'
down_revision: Union[str, Sequence[str], None] = '482db97547fb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_index('ix_transactions_account', table_name='transaction')
    op.drop_index('ix_transactions_holding_date', table_name='transaction')
    op.rename_table('transaction', 'transactions')
    op.create_index('ix_transactions_account', 'transactions', ['account_id'])
    op.create_index('ix_transactions_holding_date', 'transactions', ['holding_id', 'trade_date'])
    op.create_unique_constraint('uq_account_name_type', 'account', ['name', 'type'])
    # ### end Alembic commands ###


def downgrade() -> None:
    op.drop_constraint('uq_account_name_type', 'account', type_='unique')
    op.drop_index('ix_transactions_account', table_name='transactions')
    op.drop_index('ix_transactions_holding_date', table_name='transactions')
    op.rename_table('transactions', 'transaction')
    op.create_index('ix_transactions_account', 'transaction', ['account_id'])
    op.create_index('ix_transactions_holding_date', 'transaction', ['holding_id', 'trade_date'])
    # ### end Alembic commands ###
