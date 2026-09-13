from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select
from app.db import safe_commit, sync_records, NotFoundError
from .schemas import UpdateSchema, CreateSchema
from .models import Author, AuthorAlias


def get_all(session: Session) -> list[Author]:
    return session.execute(
        select(Author)
        .options(selectinload(Author.aliases))
    ).scalars().all()

def get(session: Session, key: int) -> Author:
    author = session.execute(
        select(Author)
        .options(selectinload(Author.aliases))
        .options(selectinload(Author.works))
        .where(Author.id == key)
    ).scalars().first()

    if author is None:
        raise NotFoundError("データが見つかりませんでした。IDを確認してください")

    return author

def create(session: Session, data: CreateSchema) -> Author:
    new_author = Author(
        name=data.name,
        yomigana=data.yomigana,
        note=data.note,
    )

    session.add(new_author)

    for alias_record in data.alias_records:
        if alias_record.alias and alias_record.alias.strip():
            new_alias = AuthorAlias(
                author=new_author,
                alias=alias_record.alias.strip()
            )
            session.add(new_alias)

    safe_commit(session)
    session.refresh(new_author)

    return new_author

def update(session: Session, key: int, data: UpdateSchema):
    author = session.get(Author, key)

    if author is None:
        raise NotFoundError("データが見つかりませんでした。IDを確認してください")

    author.name = data.name
    author.yomigana = data.yomigana
    author.note = data.note

    sync_records(
        session,
        author.aliases,
        data.alias_records,
        update=lambda alias, record: setattr(alias, "alias", record.alias),
        create=lambda record: author.aliases.append(
            AuthorAlias(alias=record.alias)
        ),
    )

    safe_commit(session)

    return author


def delete(session: Session, key: int) -> None:
    record = session.get(Author, key)

    if record is None:
        raise NotFoundError("データが見つかりませんでした。IDを確認してください")

    session.delete(record)

    safe_commit(session)