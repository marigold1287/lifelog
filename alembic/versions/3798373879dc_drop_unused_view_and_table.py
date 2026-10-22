"""drop unused view and table

Revision ID: 3798373879dc
Revises: 27918254baad
Create Date: 2026-10-23 08:51:00.178074

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3798373879dc'
down_revision: Union[str, Sequence[str], None] = '27918254baad'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


NET_WORTH_ENTRY_SQL = """
CREATE VIEW net_worth_entry AS
SELECT t.trade_date, e.account_id, e.holding_id, e.quantity
FROM entry e
JOIN transactions t ON t.id = e.transaction_id
JOIN account a ON a.id = e.account_id
WHERE a.type IN ('cash', 'bank', 'taxable', 'nisa', 'pension', 'card')
"""
 
COMPUTED_SNAPSHOT_SQL = """
CREATE VIEW computed_snapshot AS
WITH days AS (
    SELECT d.d::date AS date
    FROM generate_series(
        (SELECT min(trade_date) FROM net_worth_entry)::timestamp with time zone,
        CURRENT_DATE::timestamp with time zone,
        '1 day'::interval
    ) d(d)
), pos AS (
    SELECT d.date, t.account_id, t.holding_id, sum(t.quantity) AS qty
    FROM days d
    JOIN net_worth_entry t ON t.trade_date <= d.date
    GROUP BY d.date, t.account_id, t.holding_id
)
SELECT p.date,
       CASE
           WHEN a.type::text = 'pension'::text THEN 'pension'::character varying
           ELSE h.type
       END AS category,
       round(sum(
           p.qty *
           CASE
               WHEN h.type::text = 'cash'::text THEN 1::numeric
               ELSE pr.price
           END / h.price_per_units::numeric
       ))::bigint AS value
FROM pos p
JOIN holding h ON h.id = p.holding_id
JOIN account a ON a.id = p.account_id
LEFT JOIN LATERAL (
    SELECT price.price
    FROM price
    WHERE price.holding_id = p.holding_id AND price.price_date <= p.date
    ORDER BY price.price_date DESC
    LIMIT 1
) pr ON true
GROUP BY p.date, (
    CASE
        WHEN a.type::text = 'pension'::text THEN 'pension'::character varying
        ELSE h.type
    END
)
"""
 
DAILY_BY_CATEGORY_SQL = """
CREATE VIEW daily_by_category AS
SELECT date, category, value
FROM legacy_snapshot
WHERE date < COALESCE((SELECT min(trade_date) FROM net_worth_entry), 'infinity'::date)
UNION ALL
SELECT date, category, value
FROM computed_snapshot
"""
 
DAILY_TOTAL_SQL = """
CREATE VIEW daily_total AS
SELECT date, sum(value)::bigint AS total
FROM daily_by_category
GROUP BY date
"""

def upgrade() -> None:
    """Upgrade schema."""
    op.execute("DROP VIEW IF EXISTS daily_total")
    op.execute("DROP VIEW IF EXISTS daily_by_category")
    op.execute("DROP VIEW IF EXISTS computed_snapshot")
    op.execute("DROP VIEW IF EXISTS net_worth_entry")

    op.drop_table("legacy_snapshot")


def downgrade() -> None:
    """Downgrade schema."""

    op.create_table('legacy_snapshot',
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('category', sa.String(length=20), nullable=False),
        sa.Column('value', sa.BigInteger(), nullable=False),
        sa.CheckConstraint("category IN ('cash','fund','pension','stock')"),
        sa.PrimaryKeyConstraint('date', 'category')
    )
    op.execute(NET_WORTH_ENTRY_SQL)
    op.execute(COMPUTED_SNAPSHOT_SQL)
    op.execute(DAILY_BY_CATEGORY_SQL)
    op.execute(DAILY_TOTAL_SQL)