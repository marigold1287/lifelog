import pandas as pd
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from .models import Transaction, Account, Holding, Entry, TxType
from pathlib import Path
from app.db import SessionLocal, safe_commit
import math
import numpy as np
import unicodedata
from decimal import Decimal

PWD = Path(__file__).parent

def normalize_value(value):
    if value is None:
        return None
    if isinstance(value, str):
        return unicodedata.normalize("NFKC", value)
    return value

def create_account_mapping():
    with SessionLocal() as session:
        accounts = session.execute(select(Account).options(selectinload(Account.parent))).scalars().all()

    return {
        account.label: account
        for account in accounts
    } 

def create_income_accounts(income_categories: list[str]):
    with SessionLocal() as session:
        parent = session.scalar(
            select(Account).where(Account.name == "収入", Account.type == "income")
        )
        if parent is None:
            parent = Account(name="収入", type="income")
            session.add(parent)
            session.flush()

        existing = {child.name for child in parent.children}
        for category in income_categories:
            if category not in existing:
                parent.children.append(Account(name=category, type="income"))
                existing.add(category)

        safe_commit(session)

def create_expense_accounts(expense_accounts: list[str, str]):
    with SessionLocal() as session:
        for category, genre in expense_accounts:
            parent = session.scalar(
                select(Account).where(Account.name == category, Account.type == "expense")
            )
            if parent is None:
                parent = Account(name=category, type="expense")
                session.add(parent)
                session.flush()

            existing = {child.name for child in parent.children}
            if genre not in existing:
                parent.children.append(Account(name=genre, type="expense"))
                existing.add(genre)

        safe_commit(session)


df = pd.read_csv(PWD / "resources" / "money_diary.csv")
df = df.map(normalize_value)
df = df.astype(object).where(pd.notna(df), None)
df["date"] = pd.to_datetime(df["date"]).dt.date

is_income = (df["income"] > 0) | (df["category"] == "臨時収入")
income_categories = df.loc[is_income, "category"].drop_duplicates().tolist()

is_expense = ~is_income

income_df = df[is_income]
expense_df = df[is_expense]

income_groups = income_df.groupby(["date", "store"], dropna=False, sort=True)
expense_groups = expense_df.groupby(["date", "store"], dropna=False, sort=True)

print(len(income_df), len(expense_df), len(df))
assert len(income_df) + len(expense_df) == len(df)


expense_accounts = list(
    df.loc[is_expense, ["category", "genre"]]
    .drop_duplicates()
    .itertuples(index=False, name=None)
)

create_income_accounts(income_categories)
create_expense_accounts(expense_accounts)

account_map = create_account_mapping()

unclassified_account = account_map["未分類の支払元"]

with SessionLocal() as session:
    for (date, shop), g in income_groups:
        transaction = Transaction(
            trade_date=date,
            type="income",
            shop=shop,
        )

        total = 0
        for _, row in g.iterrows():
            account = account_map[f"収入 > {row['category']}"]
            total += row["income"]
            entry = Entry(
                account=account,
                holding_id=1,  # 円
                quantity=-row["income"],
                unit_price=Decimal(str(1.0)),
                item_name=row["item"],
                memo=row["note"],
            )
            transaction.entries.append(entry)
        if total != 0:
            entry = Entry(
                account=unclassified_account,
                holding_id=1,
                quantity=total,
                unit_price=Decimal(str(1.0)),
                item_name=None,
                memo=None,
            )
            transaction.entries.append(entry)

        session.add(transaction)

        # print(transaction.trade_date, transaction.shop)
        # for entry in transaction.entries:
        #     print("\t", entry.account.label, entry.quantity, entry.item_name, entry.memo)

    for (date, shop), g in expense_groups:
        transaction = Transaction(
            trade_date=date,
            type="expense",
            shop=shop,
        )

        total = 0
        for _, row in g.iterrows():
            account = account_map[f"{row['category']} > {row['genre']}"]
            total += row["expense"]
            entry = Entry(
                account=account,
                holding_id=1,  # 円
                quantity=row["expense"],
                unit_price=Decimal(str(1.0)),
                item_name=row["item"],
                memo=row["note"],
            )
            transaction.entries.append(entry)

        if total != 0:
            entry = Entry(
                account=unclassified_account,
                holding_id=1,
                quantity=-total,
                unit_price=Decimal(str(1.0)),
                item_name=None,
                memo=None,
            )
            transaction.entries.append(entry)

        session.add(transaction)

        # print(transaction.trade_date, transaction.shop)
        # for entry in transaction.entries:
        #     print("\t", entry.account.label, entry.quantity, entry.item_name, entry.memo)

    safe_commit(session)
