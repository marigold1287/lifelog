from sqlalchemy.orm import Session, selectinload, aliased
from sqlalchemy import select
from app.db import safe_commit, NotFoundError
from app.asset.models import Account
from .schemas import InputSchema

def get_list(session: Session) -> list[Account]:
    stmt = select(Account).options(selectinload(Account.parent)).order_by(Account.type, Account.name)
    return session.execute(stmt).scalars().all()

def get_parent_list(session: Session, exclude_key: int | None = None) -> list[Account]:
    stmt = select(Account).where(Account.parent_id.is_(None))
    if exclude_key is not None:
        stmt = stmt.where(Account.id != exclude_key)
    stmt = stmt.order_by(Account.type, Account.name)
    return session.execute(stmt).scalars().all()

def get(session: Session, key: int) -> Account:
    account = session.get(Account, key)

    if account is None:
        raise NotFoundError("データが見つかりませんでした。IDを確認してください")

    return account

def get_leaf_accounts(session: Session) -> list[Account]:
    """ツリーの末端だけを返す。
    - 子を持たない親（単独の親）
    - 子（parent_id が入っているもの）
    """
    Child = aliased(Account)

    has_children = (
        select(Child.id)
        .where(Child.parent_id == Account.id)
        .exists()
    )

    stmt = select(Account).where(~has_children)   # 自分を親にしている行がない = 葉

    stmt = stmt.order_by(Account.type, Account.name)
    return session.execute(stmt).scalars().all()


def create(session: Session, data: InputSchema) -> Account:
    account = Account(**data.model_dump())

    session.add(account)
    safe_commit(session)
    session.refresh(account)

    return account

def update(session: Session, key: int, data: InputSchema) -> Account:
    account = get(session, key)

    for field, value in data.model_dump().items():
        setattr(account, field, value)

    safe_commit(session)

    return account

def delete(session: Session, key: int) -> None:
    record = get(session, key)

    session.delete(record)

    safe_commit(session)