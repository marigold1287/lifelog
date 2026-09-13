
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select
from .models import Book
from app.book.work import Work, WorkAuthor
from app.book.publisher.models import Label, Publisher
from app.book.author.models import Author


def get_all(session: Session):
    books = session.execute(
        select(Book).options(
            selectinload(Book.work)
                .selectinload(Work.work_authors)
                .selectinload(WorkAuthor.author)
                .selectinload(Author.aliases),
            selectinload(Book.work)
                .selectinload(Work.label)
                .selectinload(Label.publisher)
                .selectinload(Publisher.aliases),
            selectinload(Book.readings),
        )
    ).scalars().all()

    return [
        record
        for book in books
        for record in book.book_list_records
    ]