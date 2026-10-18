from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select
from app.db import NotFoundError
from app.asset.models import Price

def get_latest_price(session: Session, holding_id: int) -> Price:
    price = session.execute(
        select(Price)
        .where(Price.holding_id == holding_id)
        .order_by(Price.price_date.desc())
    ).scalars().first()

    if price is None:
        raise NotFoundError("データが見つかりませんでした。IDを確認してください")

    return price