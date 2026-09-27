from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Generic, TypeVar
from app.db import safe_commit, NotFoundError
from .schemas import UpdateSchema, CreateSchema
from .base_model import BaseMixin

ModelT = TypeVar("ModelT", bound=BaseMixin)

class BaseBillRepository(Generic[ModelT]):
    model: type[ModelT]
        
    def get_record(self, session: Session, key: int):
        bill = session.get(self.model, key)

        if bill is None:
            raise NotFoundError("データが見つかりませんでした。IDを確認してください")

        return bill

    def get_providers(self, session: Session):
        return session.execute(
            select(self.model.provider).distinct()
        ).scalars().all()

    def get_all(self, session: Session) -> list[ModelT]:
        return session.execute(
            select(self.model)
            .order_by(self.model.start_date.desc())
        ).scalars().all()

    def get_latest(self, session: Session) -> ModelT | None:
        return session.execute(
            select(self.model)
            .order_by(self.model.start_date.desc())
            .limit(1)
        ).scalar_one_or_none()

    def get(self, session: Session, key: int) -> ModelT:
        return self.get_record(session, key)

    def create(self, session: Session, data: CreateSchema) -> ModelT:
        bill = self.model(**data.model_dump())

        session.add(bill)
        safe_commit(session)
        session.refresh(bill)

        return bill

    def update(self, session: Session, key: int, data: UpdateSchema) -> ModelT:
        bill = self.get_record(session, key)

        for field, value in data.model_dump().items():
            setattr(bill, field, value)

        safe_commit(session)

        return bill

    def delete(self, session: Session, key: int) -> None:
        record = self.get_record(session, key)

        session.delete(record)

        safe_commit(session)