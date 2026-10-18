"""年末調整、確定申告との統合のために給与天引き分を家計簿に移し替えるスクリプト"""
import pandas as pd
from sqlalchemy import select
from .models import Transaction, Account, Holding, Entry
from pathlib import Path
from app.db import SessionLocal, safe_commit
from app.payslip.models import Payslip

with SessionLocal() as session:
    payslips = (
        session.execute(select(Payslip).where(Payslip.seimei_hoken > 0)).scalars().all()
    )

    transactions = (
        session.execute(
            select(Transaction)
            .where(
                (Transaction.trade_date > "2017-05-01") 
              & (Transaction.trade_date < "2019-01-31")
              & (Transaction.type == "income"))
        ).scalars().all()
    )

    for payslip in payslips:
        payslip.seimei_hoken = 0

        transaction = Transaction(
            trade_date=payslip.date,
            type="expense",
            shop="第一生命",
        )
        transaction.entries.append(
            Entry(
                account_id=198,
                holding_id=1,
                quantity=3617,

            )
        )
        transaction.entries.append(
            Entry(
                account_id=171,
                holding_id=1,
                quantity=2668,
            )
        )
        transaction.entries.append(
            Entry(
                account_id=199,
                holding_id=1,
                quantity=350,
                item_name="傷害保険",
            )
        )
        transaction.entries.append(
            Entry(
                account_id=9,
                holding_id=1,
                quantity=-6635,
            )
        )

        session.add(transaction)



    for transaction in transactions:
        if transaction.note and "生命保険料調整済み" in transaction.note:
            continue

        entry_names = [entry.account.name for entry in transaction.entries]
        if "給与所得" in entry_names and "未分類の支払元" in entry_names:
            kyuyo_entry = next(
                (entry for entry in transaction.entries if entry.account.name == "給与所得"),
                None,
            )
            siharaimoto_entry = next(
                (entry for entry in transaction.entries if entry.account.name == "未分類の支払元"),
                None,
            )
            kyuyo_entry.quantity -= 6635
            siharaimoto_entry.quantity += 6635
        if transaction.note is None:
            transaction.note = "生命保険料調整済み"
        else:
            transaction.note += " 生命保険料調整済み"
            transaction.note = transaction.note.strip()

    safe_commit(session)

if __name__ == "__main__":
    print("処理済みのためこのスクリプトの実行は不要です。")