
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select
from app.db import safe_commit, sync_records, NotFoundError
from .schemas import UpdateSchema, CreateSchema, LabelRecord
from .models import Publisher, PublisherAlias, Label


def get_all(session: Session) -> list[Publisher]:
    return session.execute(
        select(Publisher)
        .options(selectinload(Publisher.aliases))
    ).scalars().all()

def get(session: Session, key: int) -> Publisher:
    publisher = session.execute(
        select(Publisher)
        .options(selectinload(Publisher.aliases))
        .options(
            selectinload(Publisher.labels)
            .selectinload(Label.works)
        )
        .where(Publisher.id == key)
    ).scalars().first()

    if publisher is None:
        raise NotFoundError("データが見つかりませんでした。IDを確認してください")

    return publisher

def create(session: Session, data: CreateSchema) -> Publisher:
    new_publisher = Publisher(
        name=data.name,
        yomigana=data.yomigana,
    )
    session.add(new_publisher)

    for alias_record in data.alias_records:
        if alias_record.alias and alias_record.alias.strip():
            session.add(
                PublisherAlias(
                    publisher=new_publisher,
                    alias=alias_record.alias.strip(),
                )
            )

    label_records = list(data.label_records)

    if not any(label.name == "レーベルなし" for label in label_records):
        label_records.append(
            LabelRecord(id=None, name="レーベルなし")
        )

    for label_record in label_records:
        if label_record.name and label_record.name.strip():
            session.add(
                Label(
                    publisher=new_publisher,
                    name=label_record.name.strip(),
                )
            )

    safe_commit(session)
    session.refresh(new_publisher)

    return new_publisher

def update(session: Session, key: int, data: UpdateSchema):
    publisher = session.get(Publisher, key)

    if publisher is None:
        raise NotFoundError("データが見つかりませんでした。IDを確認してください")

    publisher.name = data.name
    publisher.yomigana = data.yomigana

    sync_records(
        session,
        publisher.aliases,
        data.alias_records,
        update=lambda alias, record: setattr(alias, "alias", record.alias),
        create=lambda record: publisher.aliases.append(
            PublisherAlias(alias=record.alias.strip())
        ),
        is_valid=lambda record: bool(record.alias and record.alias.strip()),
    )

    sync_records(
        session,
        publisher.labels,
        data.label_records,
        update=lambda label, record: setattr(label, "name", record.name),
        create=lambda record: publisher.labels.append(
            Label(name=record.name.strip())
        ),
        is_valid=lambda record: bool(record.name and record.name.strip()),
    )

    safe_commit(session)

    return publisher


def delete(session: Session, key: int) -> None:
    publisher = session.get(Publisher, key)

    if publisher is None:
        raise NotFoundError("データが見つかりませんでした。IDを確認してください")

    session.delete(publisher)

    safe_commit(session)
