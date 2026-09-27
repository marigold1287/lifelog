
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select
from .models import Book
from app.book.work import Work


def get_all(session: Session):
    return session.execute(
        select(Book).options(
            selectinload(Book.work)
                .selectinload(Work.work_authors),
            selectinload(Book.work)
                .selectinload(Work.label),
            selectinload(Book.readings),
        )
    ).scalars().all()