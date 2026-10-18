"""integrate ledger

Revision ID: 5d8514d51426
Revises: 5cbfc098cf4b
Create Date: 2026-10-01 12:31:27.221440

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5d8514d51426'
down_revision: Union[str, Sequence[str], None] = '5cbfc098cf4b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



# 純資産に含める口座の明細だけを集める（expense / income / equity は含めない）
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
 
 
def upgrade():
    # 0. 旧テーブルに依存するVIEWを先に消す
    op.execute("DROP VIEW daily_total, daily_by_category, computed_snapshot")
 
    # 1. 旧 transactions を entry に改名し、名前の残りも整える
    op.rename_table("transactions", "entry")
    op.execute("ALTER TABLE entry RENAME CONSTRAINT transaction_pkey TO entry_pkey")
    op.execute("ALTER TABLE entry RENAME CONSTRAINT transaction_quantity_check TO entry_quantity_check")
    op.execute("ALTER TABLE entry RENAME CONSTRAINT transaction_account_id_fkey TO entry_account_id_fkey")
    op.execute("ALTER TABLE entry RENAME CONSTRAINT transaction_holding_id_fkey TO entry_holding_id_fkey")
    op.execute("ALTER SEQUENCE transaction_id_seq RENAME TO entry_id_seq")
    op.drop_index("ix_transactions_account", table_name="entry")
    op.drop_index("ix_transactions_holding_date", table_name="entry")
 
    # 2. 新しいヘッダ transactions を作る
    op.create_table(
        "transactions",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("trade_date", sa.Date, nullable=False),
        sa.Column("type", sa.String(20), nullable=False),
        sa.Column("shop", sa.String(100)),
        sa.Column("note", sa.String(500)),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )
    op.create_index("ix_transactions_trade_date", "transactions", ["trade_date"])
 
    # 3. 既存の各行と同じ id でヘッダを1つずつ作り、シーケンスを進める
    op.execute(
        """
        INSERT INTO transactions (id, trade_date, type, note, created_at)
        SELECT id, trade_date, type, note, created_at FROM entry
        """
    )
    op.execute(
        """
        SELECT setval(
            pg_get_serial_sequence('transactions', 'id'),
            COALESCE((SELECT max(id) FROM entry), 1),
            (SELECT max(id) FROM entry) IS NOT NULL
        )
        """
    )
 
    # 4. entry を明細の形にする
    op.add_column("entry", sa.Column("transaction_id", sa.Integer))
    op.execute("UPDATE entry SET transaction_id = id")
    op.alter_column("entry", "transaction_id", nullable=False)
    op.create_foreign_key(
        "entry_transaction_id_fkey",
        "entry",
        "transactions",
        ["transaction_id"],
        ["id"],
        ondelete="CASCADE",
    )
    for col in ("trade_date", "type", "note", "created_at"):
        op.drop_column("entry", col)
    op.add_column("entry", sa.Column("item_name", sa.String(200)))
    op.add_column("entry", sa.Column("memo", sa.String(500)))
    op.create_index("ix_entry_transaction", "entry", ["transaction_id"])
    op.create_index("ix_entry_account_holding", "entry", ["account_id", "holding_id"])
    op.create_index("ix_entry_holding", "entry", ["holding_id"])
 
    # 5. account に階層を持たせ、ユニーク制約を付け替える
    op.add_column("account", sa.Column("parent_id", sa.Integer))
    op.create_foreign_key(
        "account_parent_id_fkey", "account", "account", ["parent_id"], ["id"]
    )
    op.drop_constraint("uq_account_name_type", "account", type_="unique")
    op.create_unique_constraint(
        "uq_account_parent_id_name", "account", ["parent_id", "name"]
    )
    op.create_index(
        "uq_account_root_name",
        "account",
        ["name"],
        unique=True,
        postgresql_where=sa.text("parent_id IS NULL"),
    )
 
    # 6. VIEW を新しい構造で作り直す（依存順）
    op.execute(NET_WORTH_ENTRY_SQL)
    op.execute(COMPUTED_SNAPSHOT_SQL)
    op.execute(DAILY_BY_CATEGORY_SQL)
    op.execute(DAILY_TOTAL_SQL)
 
    # 円（cash）の Holding が無ければ、移行後にアプリ側かSQLで1行作る
    # （家計簿の明細はすべてこの Holding を使う）
 
 
def downgrade():
    raise NotImplementedError("pg_dump のバックアップから戻す")
