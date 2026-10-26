
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
import httpx
from datetime import date, timedelta, datetime
import asyncio
import csv
import io
from decimal import Decimal
from app.db import SessionLocal, safe_commit
from app.asset.models import Holding, Price, Entry, Transaction
import yfinance as yf

# entryで一番古いところから取得すればいい。なにもないなら取得する必要がない、といえばない。

def get_oldest_entry_date(holding: Holding, session: Session):
    return session.execute(
        select(Transaction.trade_date)
        .join(Entry, Entry.transaction_id == Transaction.id)
        .where(Entry.holding_id == holding.id)
        .order_by(Transaction.trade_date)
    ).scalars().first()

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

def get_inserted_prices(holding_id: int, session: Session):
    prices = (
        session.execute(
            select(Price)
            .where(Price.holding_id == holding_id)
            .order_by(Price.price_date.desc())
        )
        .scalars()
        .all()
    )

    return prices

def create_date_price_map(prices: list[Price]):
    return {
        price.price_date: price
        for price in prices
    }

def get_yfinance_price(holding: Holding, session: Session):
    start = get_oldest_entry_date(holding, session)
    if start is None:
        start = date.today() - timedelta(days=365)
    date_price_map = create_date_price_map(get_inserted_prices(holding.id, session))
    
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
        price = date_price_map.get(index.date())
        if price and price.source == "yfinance":
            continue
        if price:
            price.price = Decimal(str(row[holding.symbol]))
            price.source = "yfinance"
        else:
            price = Price(
                holding=holding,
                price_date=index,
                price=Decimal(str(row[holding.symbol])),
                source="yfinance",
            )
            session.add(price)

# https://emaxis.am.mufg.jp/fund/253425.html  ここからCSVを落とせるからその方が早いかもしれない...

async def get_ufj_price_from_api(holding: Holding, session: Session):
    start = get_oldest_entry_date(holding, session)
    if start is None:
        start = date.today() - timedelta(days=31)
    date_price_map = create_date_price_map(get_inserted_prices(holding.id, session))

    base_url = (
        f"https://developer.am.mufg.jp/"
        f"fund_information_date/isin_cd/{holding.symbol}/base_date/"
    )

    # 最新取得日の翌日から昨日まで
    target_date = start
    yesterday = date.today() - timedelta(days=1)

    async with httpx.AsyncClient() as client:
        while target_date <= yesterday:
            price = date_price_map.get(target_date)
            if price and price.source == "ufj":
                target_date += timedelta(days=1)
                continue

            url = f"{base_url}{target_date.strftime('%Y%m%d')}"

            response = await client.get(url)
            response.raise_for_status()

            data = response.json()


            if data["datasets"]:
                if price:
                    price.price = data["datasets"][0]["nav"]
                    price.source = "ufj"
                else:
                    price = Price(
                        holding=holding,
                        price_date=target_date,
                        price=data["datasets"][0]["nav"],
                        source="ufj",
                    )
                    session.add(price)

            target_date += timedelta(days=1)

async def get_ufj_price_from_csv(holding: Holding, session: Session):
    base_url = (
        f"https://www.am.mufg.jp/fund_file/setteirai/{holding.symbol}.csv"
    )

    date_price_map = create_date_price_map(get_inserted_prices(holding.id, session))

    async with httpx.AsyncClient() as client:
        response = await client.get(base_url)
        response.raise_for_status()

    csv_data = response.content.decode("cp932")
    f = io.StringIO(csv_data)
    next(f)

    reader = csv.DictReader(f)
    rows = list(reader)

    if not rows:
        return

    for row in rows:
        current_date = datetime.strptime(row["基準日"], "%Y/%m/%d").date()
        price = date_price_map.get(current_date)
        if price and price.source == "ufj":
            continue
        if price:
            price.price = row["基準価額(円)"]
            price.source = "ufj"
        else:
            price = Price(
                holding=holding,
                price_date=current_date,
                price=row["基準価額(円)"],
                source="ufj",
            )
            session.add(price)


async def get_rakuten_price(holding: Holding, session: Session):
    base_url = (
        f"https://www.rakuten-toushin.co.jp/assets/csv/chart_{holding.symbol}.csv"
    )

    date_price_map = create_date_price_map(get_inserted_prices(holding.id, session))

    async with httpx.AsyncClient() as client:
        response = await client.get(base_url)
        response.raise_for_status()

    reader = csv.DictReader(io.StringIO(response.text))
    rows = list(reader)

    if not rows:
        return

    for row in rows:
        current_date = datetime.strptime(row["基準日"], "%Y/%m/%d").date()
        price = date_price_map.get(current_date)
        if price and price.source == "csv":
            continue
        if price:
            price.price = row["基準価額(円)"]
            price.source = "csv"
        else:
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

    date_price_map = create_date_price_map(get_inserted_prices(holding.id, session))

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(base_url, timeout=30)
        except httpx.TimeoutException:
            return

        response.raise_for_status()

    text = response.content.decode("cp932")

    reader = csv.DictReader(io.StringIO(text))
    rows = list(reader)

    if not rows:
        return

    for row in rows:
        current_date = datetime.strptime(row["日付"], "%Y年%m月%d日").date()
        price = date_price_map.get(current_date)
        if price and price.source == "csv":
            continue
        if price:
            price.price = row["基準価額"]
            price.source = "csv"
        else:
            price = Price(
                holding=holding,
                price_date=current_date,
                price=row["基準価額"],
                source="csv",
            )
            session.add(price)

async def fetch_holding_prices(session: Session):
    result = {"success": [], "fail": []}
    holdings = (
        session.execute(
            select(Holding).where(Holding.symbol.is_not(None))
        )
        .scalars()
        .all()
    )

    for holding in holdings:
        try:
            if holding.price_source == "ufj":
                try:
                    int(holding.symbol)
                    await get_ufj_price_from_csv(holding, session)
                except ValueError:
                    await get_ufj_price_from_api(holding, session)
            if holding.price_source == "rakuten":
                await get_rakuten_price(holding, session)
            if holding.price_source == "nissei":
                await get_nissei_price(holding, session)
            if holding.price_source == "yfinance":
                get_yfinance_price(holding, session)
            result["success"].append(holding.name)
        except Exception as e:
            result["fail"].append(holding.name)

    safe_commit(session)

    return result


if __name__ == "__main__":
    with SessionLocal() as session:
        result = asyncio.run(fetch_holding_prices(session))
        print(result)

