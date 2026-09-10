
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select
from app.db import safe_commit, sync_records, NotFoundError
from .schemas import UpdateSchema, CreateSchema, BookEditSchema, AuthorSchema, PublisherSchema
from .models import Work, WorkAuthor
from app.book.book.models import Book, BookReading
from app.book.publisher.models import Label, Publisher
from app.book.author.models import Author


def get_all(session: Session) -> list[dict]:
    works = session.execute(
        select(Work).options(
            selectinload(Work.work_authors)
                .selectinload(WorkAuthor.author)
                .selectinload(Author.aliases),
            selectinload(Work.label)
                .selectinload(Label.publisher)
                .selectinload(Publisher.aliases)
        )
    ).scalars().all()

    return [work.work_record for work in works]

def get(session: Session, key: int) -> dict:
    work = session.execute(
        select(Work)
        .options(selectinload(Work.work_authors).selectinload(WorkAuthor.author).selectinload(Author.aliases))
        .options(selectinload(Work.label).selectinload(Label.publisher).selectinload(Publisher.aliases))
        .options(selectinload(Work.books).selectinload(Book.readings))
        .where(Work.id == key)
    ).scalars().first()

    if work is None:
        raise NotFoundError("データが見つかりませんでした。IDを確認してください")

    return work.work_detail_record

def create(session: Session, data: CreateSchema) -> Work:
    label = get_or_create_publisher_and_label(session, data.publisher_record, data.label, data.label_id)
    work = Work(
        title=data.title,
        label=label
    )
    session.add(work)

    for work_author in data.author_records:
        author = get_or_create_author(session, work_author)

        record  = WorkAuthor(
            work=work,
            author=author,
            role=work_author.role
        )
        session.add(record)

    for record in data.book_records:
        new_book = Book(
            title=record.title,
            volume=record.volume,
            isbn=record.isbn,
            amazon_asin=record.amazon_asin,
            registration_date=record.registration_date,
        )
        work.books.append(new_book)
        for read_record in record.read_records:
            new_book.readings.append(
                BookReading(read_date=read_record.read_date)
            )

    safe_commit(session)
    session.refresh(work)

    return work.work_detail_record

def get_or_create_author(session: Session, record: AuthorSchema):
    if record.id is None:
        return Author(
            name=record.name,
        )

    return session.get(Author, record.id)

def get_or_create_publisher_and_label(session: Session, publisher_record: PublisherSchema, label_name: str, label_id: int | None):
    if publisher_record.id is None:
        publisher = Publisher(name=publisher_record.name)
        session.add(publisher)
        label = Label(
            name=label_name,
            publisher=publisher
        )
        session.add(label)
    else:
        publisher = session.get(Publisher, publisher_record.id)
        if label_id is None:
            label = Label(
                name=label_name,
                publisher=publisher
            )
            session.add(label)
        else:
            label = session.get(Label, label_id)
    return label

def update(session: Session, key: int, data: UpdateSchema):
    work = session.get(Work, key)

    # タイトル
    work.title = data.title

    # 著者
    for work_author in work.work_authors:
        session.delete(work_author)

    for work_author in data.author_records:
        author = get_or_create_author(session, work_author)

        record  = WorkAuthor(
            work=work,
            author=author,
            role=work_author.role
        )
        session.add(record)

    # 出版社
    label = get_or_create_publisher_and_label(session, data.publisher_record, data.label, data.label_id)
    work.label = label

    # 書籍
    def update_book(current: Book, update: BookEditSchema):
        current.title = update.title
        current.volume = update.volume
        current.isbn = update.isbn
        current.amazon_asin = update.amazon_asin
        current.registration_date = update.registration_date
        
        sync_records(
            session,
            current.readings,
            update.read_records,
            update=lambda read_date, record: setattr(read_date, "read_date", record.read_date),
            create=lambda record: current.readings.append(
                BookReading(read_date=record.read_date)
            ),
        )
    def create_book(record: BookEditSchema):
        new_book = Book(
            title=record.title,
            volume=record.volume,
            isbn=record.isbn,
            amazon_asin=record.amazon_asin,
            registration_date=record.registration_date,
        )
        work.books.append(new_book)
        for read_record in record.read_records:
            new_book.readings.append(
                BookReading(read_date=read_record.read_date)
            )

    sync_records(
        session,
        work.books,
        data.book_records,
        update=update_book,
        create=create_book,
    )

    safe_commit(session)

    return work.work_detail_record


def delete(session: Session, key: int) -> None:
    work = session.get(Work, key)

    if work is None:
        raise NotFoundError("データが見つかりませんでした。IDを確認してください")

    session.delete(work)

    safe_commit(session)
