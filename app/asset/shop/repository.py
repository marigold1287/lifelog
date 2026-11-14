from sqlalchemy.orm import Session, selectinload, aliased
from sqlalchemy import select, func, literal
from app.db import safe_commit, NotFoundError, sync_records
from app.asset.models import Shop, ShopAlias, Transaction
# from .schemas import InputSchema, EntryInputSchema
from app.asset.price.repository import create_or_get_price_from_entry

def get_list(session: Session) -> list[Shop]:
    stmt = select(Shop).order_by(Shop.name)
    return session.execute(stmt).scalars().all()

def get_shop_name_list(session: Session):
    stmt = select(Transaction.shop).where(Transaction.shop.is_not(None)).distinct().order_by(Transaction.trade_date.desc())

    return session.execute(stmt).scalars().all()



def get(session: Session, key: int) -> Shop:
    stmt = (
        select(Shop)
        .where(Shop.id == key)
    )
    shop = session.execute(stmt).scalars().first()

    if shop is None:
        raise NotFoundError("データが見つかりませんでした。IDを確認してください")
    
    return shop
