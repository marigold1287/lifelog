import pandas as pd
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from .models import Transaction, Account, Holding, Entry, TxType
from pathlib import Path
from app.db import SessionLocal, safe_commit
from dateutil.relativedelta import relativedelta
import math

"""
カタリバ: 東京都
CFC: 東京都および墨田区
JASSO: 神奈川県および横浜市
UNHCR: 東京都および港区 決済代行会社から国連UNHCR協会へ入金された日（ご寄付受領日）となります。
WFP: 神奈川県および横浜市。カード引き落としされた2ヶ月後にWFPに入金される

支払いした日と各団体に入金される日が異なるから確定申告と同期させるには扱いが難しい。
"""

with SessionLocal() as session:
    entries = session.execute(
        select(Entry).options(selectinload(Entry.transaction))
        .where(Entry.account_id == 208)
    ).scalars().all()

    for entry in entries:
        if entry.transaction.shop == "独立行政法人日本学生支援機構":
            pass
        elif entry.transaction.shop == "UNHCR":
            pass
        elif entry.transaction.shop == "国連WFP協会":
            pass
        elif entry.transaction.shop == "ふるさと納税" or entry.transaction.shop == "楽天市場":
            pass
        elif entry.transaction.shop == "CFC":
            pass
        elif entry.transaction.shop == "認定NPO法人カタリバ":
            pass
        elif entry.item_name == "赤い羽根共同募金":
            pass
        else:
            print("UNKNOWN", entry.item_name, entry.transaction.shop)

    safe_commit(session)