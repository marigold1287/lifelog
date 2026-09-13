from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db import safe_commit, NotFoundError
from .schemas import UpdateSchema, CreateSchema
from .models import ElectricBill as Bill

def get_record(session: Session, key: int):
    bill = session.get(Bill, key)

    if bill is None:
        raise NotFoundError("データが見つかりませんでした。IDを確認してください")

    return bill
    

def get_all(session: Session) -> list[Bill]:
    return session.execute(
        select(Bill)
        .order_by(Bill.start_date.desc())
    ).scalars().all()

def get(session: Session, key: int) -> Bill:
    return get_record(session, key)

def create(session: Session, data: CreateSchema) -> Bill:
    bill = Bill(
        start_date=data.start_date,
        end_date=data.end_date,
        total=data.total,
        usage=data.usage,
        provider=data.provider,
    )

    session.add(bill)

    safe_commit(session)
    session.refresh(bill)

    return bill

def update(session: Session, key: int, data: UpdateSchema) -> Bill:
    bill = get_record(session, key)

    bill.start_date = data.start_date
    bill.end_date = data.end_date
    bill.total = data.total
    bill.usage = data.usage
    bill.provider = data.provider

    safe_commit(session)

    return bill

def delete(session: Session, key: int) -> None:
    record = get_record(session, key)

    session.delete(record)

    safe_commit(session)