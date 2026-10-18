import pandas as pd
from sqlalchemy import select
from .models import Transaction, Account, Holding, Entry, TxType
from pathlib import Path
from app.db import SessionLocal, safe_commit
import math

PWD = Path(__file__).parent

bank_df = pd.read_csv(PWD / "resources" / "ideco_rakuten_bank.csv").sort_values("取引日").reset_index(drop=True)
ideco_df = pd.read_csv(PWD / "resources" / "iDECO.csv").sort_values("約定日").reset_index(drop=True)


with SessionLocal() as session:
    account_ideco = session.get(Account, 25)
    holding_yen = session.get(Holding, 1)
    account_kari = session.get(Account, 17)
    holding_kari = session.get(Holding, 21)

    print(account_ideco.name, holding_yen.name, holding_kari.name, account_kari.name)
    for _, row in bank_df.iterrows():
        transaction = Transaction(
            trade_date=row["取引日"],
            type=TxType.DEPOSIT,
            note="iDeCo入金"
        )

        transaction.entries.append(
            Entry(
                account_id=25,  # iDeCo
                holding_id=1,
                quantity=row[" 入出金(円)"],
                unit_price=1.0,
            )
        )

        transaction.entries.append(
            Entry(
                account_id=17,  # 仮口座
                holding_id=21,  # 仮投信
                quantity=-row[" 入出金(円)"],
                unit_price=1.0,
            )
        )

        session.add(transaction)

    total_cost = 0.0
    total_kuchisu = 0
    total_profit_loss = 0
    for index, row in ideco_df.iterrows():
        transaction = Transaction(
            trade_date=row["約定日"],
            type=TxType.ADJUST,
            note="含み益調整"
        )

        deposit = int(bank_df.loc[index, " 入出金(円)"])

        
        total_kuchisu += row["約定数量"]
        total_cost += row["約定数量"] * row["約定単価"] / 10000.0
        average_cost = total_cost / total_kuchisu * 10000

        profit_loss = total_kuchisu * row["約定単価"] / 10000 - average_cost * total_kuchisu / 10000
        total_profit_loss += profit_loss

        print(transaction.trade_date, profit_loss, total_profit_loss)

        total_cost = total_kuchisu * row["約定単価"] / 10000.0


        transaction.entries.append(
            Entry(
                account_id=17,  # 仮口座
                holding_id=21,  # 仮投信
                quantity=-round(profit_loss),
                unit_price=1.0,
            )
        )


        session.add(transaction)

        buy_transaction = Transaction(
            trade_date=row["約定日"],
            type=TxType.BUY,
            note="iDeCo約定"
        )
        
        buy_transaction.entries.append(
            Entry(
                account_id=25,  # iDeCo
                holding_id=14,  # 楽天インデックス投信
                quantity=row["約定数量"],
                unit_price=row["約定単価"],
            )
        )

        buy_transaction.entries.append(
            Entry(
                account_id=144,  # その他-その他 費用
                holding_id=1,  # 円
                quantity=int(deposit - row["精算金額"]),
                unit_price=1.0,
                memo="iDeCo月額手数料",
            )
        )

        buy_transaction.entries.append(
            Entry(
                account_id=25,  # iDeCo
                holding_id=1,  # 円
                quantity=-deposit,
                unit_price=1.0,
            )
        )

        session.add(buy_transaction)

    safe_commit(session)


if __name__ == "__main__":
    print("移行済みのため実行不要です")
    pass