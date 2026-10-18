from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select
from app.db import safe_commit, NotFoundError
from .schemas import UpdateSchema, CreateSchema
from .models import Subsidy
from .donation.models import DonationDeduction

def get_all(session: Session) -> list[Subsidy]:
    return session.execute(
        select(Subsidy).options(selectinload(Subsidy.donations).selectinload(DonationDeduction.entry)).order_by(Subsidy.year)
    ).scalars().all()

def get(session: Session, key: int) -> Subsidy:
    record = session.get(Subsidy, key)

    if record is None:
        raise NotFoundError("データが見つかりませんでした。IDを確認してください")

    return record


def create(session: Session, data: CreateSchema) -> Subsidy:
    record = Subsidy(**data.model_dump())

    session.add(record)
    safe_commit(session)
    session.refresh(record)

    return record

def update(session: Session, key: int, data: UpdateSchema) -> Subsidy:
    record = get(session, key)

    for field, value in data.model_dump().items():
        setattr(record, field, value)

    safe_commit(session)

    return record

def delete(session: Session, key: int) -> None:
    record = get(session, key)

    session.delete(record)

    safe_commit(session)