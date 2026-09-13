from app.book.publisher import Publisher, PublisherAlias
from app.book.publisher import repository, schemas
from sqlalchemy import select
import pytest
from app.db import DomainValidationError
from pydantic import ValidationError

@pytest.fixture
def publisher_create():
    return schemas.CreateSchema(
        name="講談社",
        yomigana="こうだんしゃ",
        alias_records=[{"id": None, "alias": "Kodansha"}]
    )

def test_spaces_publisher_create():
    with pytest.raises(ValidationError) as exc_info:
        schemas.CreateSchema(
            name="    ",
            yomigana="こうだんしゃ",
            alias_records=[{"id": None, "alias": "Kodansha"}],
        )

@pytest.fixture
def publisher(session):
    publisher = Publisher(
        name="講談社",
        yomigana="こうだんしゃ"
    )
    session.add(publisher)
    alias = PublisherAlias(
        alias="Kodansha",
        publisher=publisher
    )
    session.add(alias)
    session.flush()
    return publisher


def test_create_repository(publisher_create, session):
    publisher = repository.create(session, publisher_create)

    assert publisher.id is not None

def test_update_repository(publisher, session):
    current = schemas.UpdateSchema.model_validate(publisher)
    current.yomigana = "こうだんしゃかい"
    current.alias_records[0].alias = "Kodansha-Kai"

    updated = repository.update(session, publisher.id, current)

    assert updated.yomigana == "こうだんしゃかい"


# 正常系テスト
def test_publisher_insert_success(session):
    publisher = Publisher(name="hoge")
    session.add(publisher)
    session.commit()

    assert publisher.id is not None

# 異常系テスト（空文字バリデーションの検証）
def test_publisher_insert_empty_name_fails(session):
    with pytest.raises(DomainValidationError):
        Publisher(name="")

def test_no_publisher(session):
    publishers = session.execute(select(Publisher)).scalars().all()

    assert len(publishers) == 0