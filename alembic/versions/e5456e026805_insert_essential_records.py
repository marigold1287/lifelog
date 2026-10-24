"""insert essential records

Revision ID: e5456e026805
Revises: 3798373879dc
Create Date: 2026-10-23 09:23:53.532411

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from pathlib import Path
import json
import datetime as dt

PWD = Path(__file__).parent

records_dir = PWD.parent / "records"

with open(records_dir / "account.json") as f:
    accounts = json.load(f)

with open(records_dir / "holding.json") as f:
    holdings = json.load(f)

account_table = sa.Table(
    "account",
    sa.MetaData(),
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("name", sa.String(100)),
    sa.Column(
        "type",
        sa.Enum("cash", "bank", "taxable", "nisa", "pension", "card", "expense", "income", "equity",
                name="account_type"),
    ),
    sa.Column("currency", sa.String(3)),
    sa.Column("sort_order", sa.Integer),
    sa.Column("parent_id", sa.Integer),
)

holding_table = sa.Table(
    "holding",
    sa.MetaData(),
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("name", sa.String(100)),
    sa.Column(
        "type",
        sa.Enum("cash", "fund", "stock",
                name="holding_type"),
    ),
    sa.Column("currency", sa.String(3)),
    sa.Column("symbol", sa.String(50)),
    sa.Column("price_source", sa.String(50)),
    sa.Column("price_per_units", sa.Integer),
)

price_table = sa.Table(
    "price",
    sa.MetaData(),
    sa.Column("holding_id", sa.Integer, primary_key=True),
    sa.Column("price_date", sa.Date),
    sa.Column("price", sa.Numeric(20, 6)),
    sa.Column("source", sa.String(50)),
)

# revision identifiers, used by Alembic.
revision: str = 'e5456e026805'
down_revision: Union[str, Sequence[str], None] = '3798373879dc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def _get_or_create(conn, name, type_, currency, sort_order, parent_id):
    parent_cond = (
        account_table.c.parent_id.is_(None)
        if parent_id is None
        else account_table.c.parent_id == parent_id
    )
    existing = conn.execute(
        sa.select(account_table.c.id).where(
            account_table.c.name == name, parent_cond
        )
    ).scalar()
    if existing is not None:
        return existing

    res = conn.execute(
        account_table.insert().values(
            name=name,
            type=type_,
            currency=currency,
            sort_order=sort_order,
            parent_id=parent_id,
        )
    )
    return res.inserted_primary_key[0]


def upgrade() -> None:
    conn = op.get_bind()

    # これらのアカウントが一つも存在しない場合はサンプルも兼ねてjsonに書き込まれたアカウント情報を登録する
    already_existing = []
    for t in ["cash", "card", "bank", "nisa", "pension", "taxable"]:
        existing = conn.execute(
            sa.select(account_table.c.id).where(
                account_table.c.type == t
            )
        ).scalar()
        
        if existing is not None:
            already_existing.append(t)

    for parent_name, value in accounts.items():
        if value["type"] not in already_existing:
            parent_id = _get_or_create(
                conn, parent_name, value["type"], value["currency"],
                value["sort_order"], None,
            )
            for c in value.get("children", []):
                _get_or_create(
                    conn, c["name"], c["type"], c["currency"],
                    c["sort_order"], parent_id,
                )

    for holding_name, value in holdings.items():
        holding_id = conn.execute(
            sa.select(holding_table.c.id).where(
                holding_table.c.name == holding_name,
            )
        ).scalar()

        if holding_id is None:
            res = conn.execute(
                holding_table.insert().values(
                    name=holding_name,
                    type=value["type"],
                    currency=value["currency"],
                    symbol=value.get("symbol", None),
                    price_source=value.get("price_source", None),
                    price_per_units=value.get("price_per_units", 1),
                )
            )
            holding_id = res.inserted_primary_key[0]

        price_date = conn.execute(
            sa.select(price_table.c.price_date).where(
                price_table.c.holding_id == holding_id,
            ).order_by(price_table.c.price_date.desc())
        ).scalar()

        if price_date is None:
            conn.execute(
                price_table.insert().values(
                    holding_id=holding_id,
                    price_date=dt.date(1900, 1, 1),
                    price=value.get("price_per_units", 1),
                    source="initial",
                )
            )


def downgrade() -> None:
    """Downgrade schema."""
    pass
