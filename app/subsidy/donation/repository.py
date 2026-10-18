from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select, or_
from app.db import safe_commit, NotFoundError
from .schemas import UpdateSchema, CreateSchema
from .models import DonationDeduction
from app.asset.models import Entry, Account, Transaction

def get_all(session: Session) -> list[DonationDeduction]:
    return session.execute(
        select(DonationDeduction)
        .join(Entry, DonationDeduction.entry_id == Entry.id)
        .join(Transaction, Entry.transaction_id == Transaction.id)
        .options(selectinload(DonationDeduction.entry))
        .order_by(Transaction.trade_date.desc())
    ).scalars().all()

def get(session: Session, key: int) -> DonationDeduction:
    record = session.get(DonationDeduction, key)

    if record is None:
        raise NotFoundError("データが見つかりませんでした。IDを確認してください")

    return record

def get_entries_without_donation_deduction(
    session: Session,
    entry_id: int | None = None,
) -> list[Entry]:
    donation_account = session.scalars(
        select(Account).where(
            Account.name == "寄附金控除対象寄附金",
        )
    ).first()

    if donation_account is None:
        return []

    eligible = (
        Entry.account.has(Account.id == donation_account.id)
        & Entry.id.not_in(select(DonationDeduction.entry_id))
    )

    stmt = select(Entry).where(eligible)

    if entry_id is not None:
        stmt = select(Entry).where(
            or_(eligible, Entry.id == entry_id)
        )

    return session.scalars(stmt).all()

def create(session: Session, data: CreateSchema) -> DonationDeduction:
    record = DonationDeduction(**data.model_dump())

    session.add(record)
    safe_commit(session)
    session.refresh(record)

    return record

def update(session: Session, key: int, data: UpdateSchema) -> DonationDeduction:
    record = get(session, key)

    for field, value in data.model_dump().items():
        setattr(record, field, value)

    safe_commit(session)

    return record

def delete(session: Session, key: int) -> None:
    record = get(session, key)

    session.delete(record)

    safe_commit(session)