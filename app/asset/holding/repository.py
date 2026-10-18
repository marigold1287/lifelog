from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select
from app.db import safe_commit, NotFoundError
from app.asset.models import Holding, Entry
from .schemas import InputSchema

def get_list(session: Session) -> list[Holding]:
    stmt = select(Holding)
    return session.execute(stmt).scalars().all()

def get(session: Session, key: int) -> Holding:
    holding = session.execute(
        select(Holding).options(
            selectinload(Holding.entries).selectinload(Entry.transaction),
            selectinload(Holding.entries).selectinload(Entry.account),
        )
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