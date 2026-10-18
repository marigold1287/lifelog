import pandas as pd
from .models import Transaction, Account, Holding, Entry
from pathlib import Path
from app.db import SessionLocal, safe_commit
import math

PWD = Path(__file__).parent


df = pd.read_csv(PWD / "resources" / "asset.csv")

df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")

first_idx = df.index[0]

print(df, first_idx)
month_end_idx = (
    df.groupby(df["date"].dt.to_period("M"))["date"]
    .idxmax()
)

selected_idx = [first_idx, *month_end_idx]
selected_idx = sorted(set(selected_idx))

df = df.loc[selected_idx].sort_values("date")


# 現金を仮口座に積み上げる
df["cash_diff"] = df["cash"].diff().fillna(0)
df["fund_diff"] = df["investment_trust"].diff().fillna(0)
df["pension_diff"] = df["pension"].diff().fillna(0)

print(df)

with SessionLocal() as session:
    bank = session.get(Account, 16)
    pension = session.get(Account, 17)
    yen = session.get(Holding, 1)
    fund = session.get(Holding, 21)

    for _, row in df.iterrows():

        transaction = Transaction(
            trade_date=row["date"],
            type="adjust",
        )
        transaction.entries.append(Entry(
            transaction=transaction,
            holding=yen,
            account=bank,
            quantity=row["cash_diff"],
        ))
        transaction.entries.append(Entry(
            transaction=transaction,
            holding=fund,
            account=bank,
            quantity=row["fund_diff"],
        ))
        transaction.entries.append(Entry(
            transaction=transaction,
            holding=fund,
            account=pension,
            quantity=row["pension_diff"],
        ))
        session.add(transaction)
    safe_commit(session)
