"""create views

Revision ID: 482db97547fb
Revises: 05abafea776d
Create Date: 2026-09-30 10:09:13.441924

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '482db97547fb'
down_revision: Union[str, Sequence[str], None] = '05abafea776d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# SQLはmodels.pyからimportせず、このファイルに固定して持つ。
# （後で models.py を書き換えても、過去のマイグレーションの内容が変わらないように）
COMPUTED_SNAPSHOT = """
CREATE OR REPLACE VIEW computed_snapshot AS
WITH days AS (
    SELECT d::date AS date
    FROM generate_series(
        (SELECT MIN(trade_date) FROM transaction),
        CURRENT_DATE,
        interval '1 day'
    ) AS d
),
pos AS (
    SELECT d.date, t.account_id, t.holding_id, SUM(t.quantity) AS qty
    FROM days d
    JOIN transaction t ON t.trade_date <= d.date
    GROUP BY d.date, t.account_id, t.holding_id
)
SELECT
    p.date,
    CASE WHEN a.type = 'pension' THEN 'pension' ELSE h.type END AS category,
    ROUND(SUM(
        p.qty
        * CASE WHEN h.type = 'cash' THEN 1 ELSE pr.price END
        / h.price_per_units
    ))::bigint AS value
FROM pos p
JOIN holding h ON h.id = p.holding_id
JOIN account a ON a.id = p.account_id
LEFT JOIN LATERAL (
    SELECT price FROM price
    WHERE holding_id = p.holding_id AND price_date <= p.date
    ORDER BY price_date DESC
    LIMIT 1
) pr ON TRUE
GROUP BY p.date, CASE WHEN a.type = 'pension' THEN 'pension' ELSE h.type END
"""
 
DAILY_BY_CATEGORY = """
CREATE OR REPLACE VIEW daily_by_category AS
SELECT date, category, value
FROM legacy_snapshot
WHERE date < COALESCE((SELECT MIN(trade_date) FROM transaction), 'infinity'::date)
UNION ALL
SELECT date, category, value
FROM computed_snapshot
"""
 
DAILY_TOTAL = """
CREATE OR REPLACE VIEW daily_total AS
SELECT date, SUM(value)::bigint AS total
FROM daily_by_category
GROUP BY date
"""
 


def upgrade() -> None:
    # 依存の順（下のVIEWから）に作る
    op.execute(COMPUTED_SNAPSHOT)
    op.execute(DAILY_BY_CATEGORY)
    op.execute(DAILY_TOTAL)
 
 
def downgrade() -> None:
    # 逆順（上のVIEWから）に消す
    op.execute("DROP VIEW IF EXISTS daily_total")
    op.execute("DROP VIEW IF EXISTS daily_by_category")
    op.execute("DROP VIEW IF EXISTS computed_snapshot")
 
