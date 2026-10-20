from sqlalchemy.orm import Session
from sqlalchemy import select, func
from app.db import safe_commit, NotFoundError
from .schemas import UpdateSchema, CreateSchema
from .models import HealthCheckup

def get_all(session: Session) -> list[HealthCheckup]:
    return session.execute(
        select(HealthCheckup).order_by(HealthCheckup.date.desc())
    ).scalars().all()

def get(session: Session, key: int) -> HealthCheckup:
    record = session.get(HealthCheckup, key)

    if record is None:
        raise NotFoundError("データが見つかりませんでした。IDを確認してください")

    return record



def create(session: Session, data: CreateSchema) -> HealthCheckup:
    record = HealthCheckup(**data.model_dump())

    session.add(record)
    safe_commit(session)
    session.refresh(record)

    return record

def update(session: Session, key: int, data: UpdateSchema) -> HealthCheckup:
    record = get(session, key)

    for field, value in data.model_dump().items():
        setattr(record, field, value)

    safe_commit(session)

    return record

def delete(session: Session, key: int) -> None:
    record = get(session, key)

    session.delete(record)

    safe_commit(session)
