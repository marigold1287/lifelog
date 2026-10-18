from sqlalchemy.orm import Session
from sqlalchemy import select, func
from app.db import safe_commit, NotFoundError
from .schemas import UpdateSchema, CreateSchema
from .models import Payslip

def get_all(session: Session) -> list[Payslip]:
    return session.execute(
        select(Payslip)
    ).scalars().all()

def get(session: Session, key: int) -> Payslip:
    record = session.get(Payslip, key)

    if record is None:
        raise NotFoundError("データが見つかりませんでした。IDを確認してください")

    return record


def get_latest(session: Session) -> Payslip | None:
    return session.execute(
        select(Payslip)
        .order_by(Payslip.date.desc())
        .limit(1)
    ).scalar_one_or_none()


def create(session: Session, data: CreateSchema) -> Payslip:
    record = Payslip(**data.model_dump())

    session.add(record)
    safe_commit(session)
    session.refresh(record)

    return record

def update(session: Session, key: int, data: UpdateSchema) -> Payslip:
    record = get(session, key)

    for field, value in data.model_dump().items():
        setattr(record, field, value)

    safe_commit(session)

    return record

def delete(session: Session, key: int) -> None:
    record = get(session, key)

    session.delete(record)

    safe_commit(session)


def get_deduction_total_by_date(
    session: Session,
):
    stmt = (
        select(
            Payslip.date,
            func.sum(Payslip.total_shikyu).label("nenshu"),
            func.sum(Payslip.tsukin_teate).label("tsukin_teate"),
            func.sum(Payslip.kenko_hoken + Payslip.kosei_nenkin + Payslip.koyo_hoken + Payslip.kodomo_shienkin).label("shakai_hoken_ryo"),
            func.sum(Payslip.shotoku_zei).label("shotoku_zei"),
        )
        .group_by(Payslip.date)
        .order_by(Payslip.date)
    )

    return session.execute(stmt).all()
