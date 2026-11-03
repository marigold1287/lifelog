from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select, func
from app.db import safe_commit, NotFoundError
from app.asset.models import Holding, Entry, Account, AccountType
from .schemas import InputSchema, AccountSummarySchema

def get_list(session: Session) -> list[Holding]:
    stmt = select(Holding)
    return session.execute(stmt).scalars().all()

def get_holding_summaries(session: Session):
    return session.execute(
        select(
            Holding.id,
            Holding.name,
            Holding.type,
            Holding.symbol,
            Holding.price_per_units,
            func.sum(Entry.quantity).label("total_quantity"),
            func.sum(Entry.quantity * Entry.unit_price / Holding.price_per_units).label("acquisition_cost"),
        )
        .join(Holding, Entry.holding_id == Holding.id)
        .join(Account, Entry.account_id == Account.id)
        .where(
            Account.type.notin_(
                [AccountType.EXPENSE,
                AccountType.INCOME,
                AccountType.EQUITY,]
            )
        )
        .group_by(
            Holding.id,
            Holding.name,
            Holding.type,
            Holding.symbol,
            Holding.price_per_units,
        )
    ).mappings().all()

def get_account_summaries(session: Session, key: int) -> list[AccountSummarySchema]:
    return session.execute(
        select(
            Account.name,
            Holding.price_per_units,
            func.sum(Entry.quantity).label("total_quantity"),
            func.sum(Entry.quantity * Entry.unit_price / Holding.price_per_units).label("acquisition_cost"),
        )
        .join(Holding, Entry.holding_id == Holding.id)
        .join(Account, Entry.account_id == Account.id)
        .where(
            Account.type.notin_(
                [AccountType.EXPENSE,
                AccountType.INCOME,
                AccountType.EQUITY,]
            ),
            Holding.id == key,
        )
        .group_by(
            Holding.price_per_units,
            Account.name,
        )
    ).mappings().all()

def get(session: Session, key: int) -> Holding:
    holding = session.execute(
        select(Holding)
        .where(Holding.id == key)
    ).scalars().first()

    if holding is None:
        raise NotFoundError("データが見つかりませんでした。IDを確認してください")

    return holding

def create(session: Session, data: InputSchema) -> Holding:
    holding = Holding(**data.model_dump())

    session.add(holding)
    safe_commit(session)
    session.refresh(holding)

    return holding

def update(session: Session, key: int, data: InputSchema) -> Holding:
    holding = get(session, key)

    for field, value in data.model_dump().items():
        setattr(holding, field, value)

    safe_commit(session)

    return holding

def delete(session: Session, key: int) -> None:
    record = get(session, key)

    session.delete(record)

    safe_commit(session)