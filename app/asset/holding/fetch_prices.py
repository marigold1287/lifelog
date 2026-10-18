
from sqlalchemy import select
from sqlalchemy.orm import Session
import httpx
from datetime import date, timedelta, datetime
import asyncio
import csv
import io
from decimal import Decimal
from app.db import SessionLocal, safe_commit
from app.asset.models import Holding, Price
import yfinance as yf

def get_yfinance_price(holding: Holding, session: Session):
    start = get_latest_price_date(holding.id, session) or date(2016, 3, 31)
    start += timedelta(days=1)

    if start >= date.today():
        return

    df = yf.download(
        [holding.symbol],
        start=start,
        auto_adjust=False,
    )["Close"]

    # yfinanceから返ってきたデータを明示的に開始日以降へ限定
    df = df[df.index.date >= start]
    df = df.dropna(subset=[holding.symbol])

    if df.empty:
        return []

    if holding.currency == "USD":
        fx = yf.download(
            ["USDJPY=X"],
            start=start,
            auto_adjust=False,
        )["Close"]

        fx = fx[fx.index.date >= start]

        df = df.join(fx)

        # 株価・為替の両方が存在する日だけ残す
        df = df.dropna(subset=[holding.symbol, "USDJPY=X"])

        # USD → JPY
        df[holding.symbol] *= df["USDJPY=X"]

        df = df.drop(columns=["USDJPY=X"])

    for index, row in df.iterrows():
        price = Price(
            holding=holding,
            price_date=index,
            price=Decimal(str(row[holding.symbol])),
            source="yfinance",
        )
        session.add(price)



def get_latest_price_date(holding_id: int, session: Session):
    latest_price_date = (
        session.execute(
            select(Price.price_date)
            .where(Price.holding_id == holding_id)
            .order_by(Price.price_date.desc())
        )
        .scalars()
        .first()
    )

    return latest_price_date

async def get_ufj_price(holding: Holding, session: Session):
    FETCH_START_DATE = date(2026, 8, 31)

    base_url = (
        f"https://developer.am.mufg.jp/"
        f"fund_information_date/isin_cd/{holding.symbol}/base_date/"
    )

    latest_price_date = get_latest_price_date(holding.id, session) or FETCH_START_DATE

    # 最新取得日の翌日から昨日まで
    target_date = latest_price_date + timedelta(days=1)
    yesterday = date.today() - timedelta(days=1)

    async with httpx.AsyncClient() as client:
        while target_date <= yesterday:
            url = f"{base_url}{target_date.strftime('%Y%m%d')}"

            response = await client.get(url)
            response.raise_for_status()

            data = response.json()


            if data["datasets"]:
                price = Price(
                    holding=holding,
                    price_date=target_date,
                    price=data["datasets"][0]["nav"],
                    source="api",
                )
                session.add(price)

            target_date += timedelta(days=1)



async def get_rakuten_price(holding: Holding, session: Session):
    base_url = (
        f"https://www.rakuten-toushin.co.jp/assets/csv/chart_{holding.symbol}.csv"
    )

    latest_price_date = get_latest_price_date(holding.id, session)

    async with httpx.AsyncClient() as client:
        response = await client.get(base_url)
        response.raise_for_status()

    reader = csv.DictReader(io.StringIO(response.text))
    rows = list(reader)

    if not rows:
        return

    if not latest_price_date:
        target_date = datetime.strptime(
            rows[0]["基準日"],
            "%Y/%m/%d"
        ).date()
    else:
        target_date = latest_price_date + timedelta(days=1)


    for row in rows:
        current_date = datetime.strptime(row["基準日"], "%Y/%m/%d").date()
        if current_date >= target_date:
            price = Price(
                holding=holding,
                price_date=current_date,
                price=row["基準価額(円)"],
                source="csv",
            )
            session.add(price)


async def get_nissei_price(holding: Holding, session: Session):
    base_url = (
        f"https://www.nam.co.jp/fundinfo/data/csv.php?fund_code={holding.symbol}"
    )

    latest_price_date = get_latest_price_date(holding.id, session)

    async with httpx.AsyncClient() as client:
        response = await client.get(base_url)
        response.raise_for_status()

    text = response.content.decode("cp932")

    reader = csv.DictReader(io.StringIO(text))
    rows = list(reader)

    if not rows:
        return

    if not latest_price_date:
        target_date = datetime.strptime(
            rows[-1]["日付"],
            "%Y年%m月%d日"
        ).date()
    else:
        target_date = latest_price_date + timedelta(days=1)


    for row in rows:
        current_date = datetime.strptime(row["日付"], "%Y年%m月%d日").date()
        if current_date >= target_date:
            price = Price(
                holding=holding,
                price_date=current_date,
                price=row["基準価額"],
                source="csv",
            )
            session.add(price)

async def main():
    with SessionLocal() as session:
        holdings = (
            session.execute(
                select(Holding).where(Holding.symbol.is_not(None))
            )
            .scalars()
            .all()
        )

        for holding in holdings:
            if holding.price_source == "ufj":
                await get_ufj_price(holding, session)
            if holding.price_source == "rakuten":
                await get_rakuten_price(holding, session)
            if holding.price_source == "nissei":
                await get_nissei_price(holding, session)
            if holding.price_source == "yfinance":
                get_yfinance_price(holding, session)

        safe_commit(session)

if __name__ == "__main__":
    asyncio.run(main())


