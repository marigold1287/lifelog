import pandas as pd
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.asset.models import Entry, Account
from .models import DonationDeduction
from .repository import get_entries_without_donation_deduction
from .schemas import to_entry_list_schema
from pathlib import Path
from app.db import SessionLocal, safe_commit
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
    entries = get_entries_without_donation_deduction(session)
    account = session.execute(select(Account).where(Account.name == "寄附金控除対象寄附金")).scalars().first()

    for entry in entries:
        record = session.get(DonationDeduction, entry.id)
        if entry.transaction.shop == "独立行政法人日本学生支援機構":
            entry.account_id = account.id
            record = DonationDeduction(
                entry_id=entry.id,
                is_shimin_zei_deduction = False,
                is_kenmin_zei_deduction = False,
                is_shotoku_zei_deduction = True,
                deduction_year = entry.transaction.trade_date.year,
            )
            session.add(record)
        elif entry.transaction.shop == "UNHCR":
            entry.account_id = account.id
            record = DonationDeduction(
                entry_id=entry.id,
                is_shimin_zei_deduction = False,
                is_kenmin_zei_deduction = True,
                is_shotoku_zei_deduction = True,
                deduction_year = entry.transaction.trade_date.year,
            )
            session.add(record)
        elif entry.transaction.shop == "国連WFP協会":
            entry.account_id = account.id
            record = DonationDeduction(
                entry_id=entry.id,
                is_shimin_zei_deduction = False,
                is_kenmin_zei_deduction = False,
                is_shotoku_zei_deduction = True,
                deduction_year = entry.transaction.trade_date.year,
            )
            session.add(record)
        elif entry.transaction.shop == "ふるさと納税" or entry.transaction.shop == "楽天市場":
            entry.account_id = 201
        elif entry.transaction.shop == "CFC":
            entry.account_id = account.id
            record = DonationDeduction(
                entry_id=entry.id,
                is_shimin_zei_deduction = False,
                is_kenmin_zei_deduction = True,
                is_shotoku_zei_deduction = True,
                deduction_year = entry.transaction.trade_date.year,
            )
            session.add(record)
        elif entry.transaction.shop == "認定NPO法人カタリバ":
            entry.account_id = account.id
            record = DonationDeduction(
                entry_id=entry.id,
                is_shimin_zei_deduction = False,
                is_kenmin_zei_deduction = True,
                is_shotoku_zei_deduction = True,
                deduction_year = entry.transaction.trade_date.year,
            )
            session.add(record)
        elif entry.item_name == "赤い羽根共同募金":
            entry.account_id = 205
        else:
            print("UNKNOWN", entry.item_name, entry.transaction.shop)

    # safe_commit(session)