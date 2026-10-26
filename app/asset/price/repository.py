from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select, func, and_
from app.db import NotFoundError
from datetime import date
from app.asset.models import Price, Entry

def get_latest_price(session: Session, holding_id: int) -> Price | None:
    price = session.execute(
        select(Price)
        .where(Price.holding_id == holding_id)
        .order_by(Price.price_date.desc())
    ).scalars().first()

    return price

def get_latest_prices(session: Session) -> dict[int, Price]:
    latest = (
        select(
            Price.holding_id,
            func.max(Price.price_date).label("max_date"),
        )
        .group_by(Price.holding_id)
        .subquery()
    )

    stmt = select(Price).join(
        latest,
        and_(
            Price.holding_id == latest.c.holding_id,
            Price.price_date == latest.c.max_date,
        ),
    )

    prices = session.execute(stmt).scalars().all()
    return {p.holding_id: p for p in prices}

def get(session: Session, holding_id: int, price_date: date) -> Price:
    price = session.execute(
        select(Price)
        .where(
            Price.holding_id == holding_id,
            Price.price_date == price_date
        )
    ).scalar()

    if price is None:
        raise NotFoundError("データが存在しません")

    return price


def create_or_get_price_from_entry(session: Session, entry: Entry):
    try:
        price = get(session, entry.holding_id, entry.transaction.trade_date)
        if price.source == "manual":
            price.price = entry.unit_price
    except NotFoundError:
        price = Price(
            holding_id=entry.holding_id,
            price_date=entry.transaction.trade_date,
            price=entry.unit_price,
            source="manual",
        )
        session.add(price)

    return price