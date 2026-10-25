from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select, func
from app.db import safe_commit, NotFoundError, sync_records
from app.asset.models import Transaction, Entry, TxType, Account, HoldingType, Holding
from .schemas import InputSchema, EntryInputSchema
from app.asset.price.repository import create_or_get_price_from_entry

def get_list(session: Session) -> list[Transaction]:
    stmt = select(Transaction).order_by(Transaction.trade_date.desc())
    return session.execute(stmt).scalars().all()

def get(session: Session, key: int) -> Transaction:
    stmt = (
        select(Transaction)
        .options(selectinload(Transaction.entries))
        .where(Transaction.id == key)
    )
    transaction = session.execute(stmt).scalars().first()

    if transaction is None:
        raise NotFoundError("データが見つかりませんでした。IDを確認してください")

    return transaction

def get_entry(session: Session, key: int) -> Entry:
    stmt = (
        select(Entry)
        .options(selectinload(Entry.transaction))
        .where(Entry.id == key)
    )
    entry = session.execute(stmt).scalars().first()

    if entry is None:
        raise NotFoundError("データが見つかりませんでした。IDを確認してください")

    return entry

def get_total_by_date(
    session: Session,
    tx_type: TxType,
    account_name: str,
):
    stmt = (
        select(
            Transaction.trade_date,
            func.sum(func.abs(Entry.quantity)).label("total"),
        )
        .join(Transaction, Entry.transaction_id == Transaction.id)
        .join(Account, Entry.account_id == Account.id)
        .where(
            Transaction.type == tx_type,
            Account.name == account_name,
        )
        .group_by(Transaction.trade_date)
        .order_by(Transaction.trade_date)
    )

    return session.execute(stmt).all()

def create(session: Session, data: InputSchema) -> Transaction:
    transaction = Transaction(
        trade_date=data.trade_date,
        type=data.type.value,
        shop=data.shop,
        note=data.note,
    )

    for entry in data.entries:
        new_entry = Entry(
                        account_id=entry.account_id,
                        holding_id=entry.holding_id,
                        quantity=entry.quantity,
                        unit_price=entry.unit_price,
                        item_name=entry.item_name,
                        memo=entry.memo,
                    )
        transaction.entries.append(new_entry)
        holding = session.get(Holding, entry.holding_id)
        if (transaction.type in [TxType.BUY, TxType.SELL]) and (holding.type in [HoldingType.FUND, HoldingType.STOCK]):
            create_or_get_price_from_entry(session, new_entry)


    session.add(transaction)
    safe_commit(session)
    session.refresh(transaction)

    return transaction

def update(session: Session, key: int, data: InputSchema) -> Transaction:
    transaction = get(session, key)

    transaction.trade_date=data.trade_date
    transaction.type=data.type
    transaction.shop=data.shop
    transaction.note=data.note

    def update_record(current: Entry, update: EntryInputSchema):
        current.account_id=update.account_id
        current.holding_id=update.holding_id
        current.quantity=update.quantity
        current.unit_price=update.unit_price
        current.item_name=update.item_name
        current.memo=update.memo
        if transaction.type in [TxType.BUY, TxType.SELL]:
            holding = session.get(Holding, update.holding_id)

            if holding.type in [HoldingType.FUND, HoldingType.STOCK]:
                create_or_get_price_from_entry(session, current)

    def create_record(record: EntryInputSchema):
        new_entry = Entry(
            account_id=record.account_id,
            holding_id=record.holding_id,
            quantity=record.quantity,
            unit_price=record.unit_price,
            item_name=record.item_name,
            memo=record.memo,
        )
        if (transaction.type in [TxType.BUY, TxType.SELL]) and (new_entry.holding.type in [HoldingType.FUND, HoldingType.STOCK]):
            create_or_get_price_from_entry(session, new_entry)
        transaction.entries.append(new_entry)

    sync_records(
        session,
        transaction.entries,
        data.entries,
        update_record,
        create_record,
    )

    safe_commit(session)

    return transaction

def delete(session: Session, key: int) -> None:
    record = get(session, key)

    session.delete(record)

    safe_commit(session)