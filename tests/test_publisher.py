import pytest
from pydantic import ValidationError
from sqlalchemy import select

from app.book.publisher import Publisher, PublisherAlias
from app.book.publisher import repository, schemas
from app.db import DomainValidationError


# =========================
# Schema
# =========================

@pytest.fixture
def publisher_create():
    return schemas.CreateSchema(
        name="講談社",
        yomigana="こうだんしゃ",
        alias_records=[
            {"id": None, "alias": "Kodansha"},
        ],
    )


def test_create_schema_success():
    schema = schemas.CreateSchema(
        name="講談社",
        yomigana="こうだんしゃ",
        alias_records=[
            {"id": None, "alias": "Kodansha"},
        ],
    )

    assert schema.name == "講談社"
    assert schema.yomigana == "こうだんしゃ"
    assert len(schema.alias_records) == 1
    assert schema.alias_records[0].alias == "Kodansha"


def test_create_schema_empty_name_fails():
    with pytest.raises(ValidationError):
        schemas.CreateSchema(
            name="",
            yomigana="こうだんしゃ",
            alias_records=[
                {"id": None, "alias": "Kodansha"},
            ],
        )


def test_create_schema_space_only_name_fails():
    with pytest.raises(ValidationError):
        schemas.CreateSchema(
            name="    ",
            yomigana="こうだんしゃ",
            alias_records=[
                {"id": None, "alias": "Kodansha"},
            ],
        )


def test_create_schema_normalizes_yomigana():
    schema = schemas.CreateSchema(
        name="講談社",
        yomigana="  こうだんしゃ  ",
        alias_records=[],
    )

    assert schema.yomigana == "こうだんしゃ"


def test_create_schema_empty_yomigana_becomes_none():
    schema = schemas.CreateSchema(
        name="講談社",
        yomigana="    ",
        alias_records=[],
    )

    assert schema.yomigana is None


@pytest.mark.parametrize(
    "alias",
    ["", "   ", None],
)
def test_create_schema_removes_empty_alias_record(alias):
    schema = schemas.CreateSchema(
        name="講談社",
        yomigana="こうだんしゃ",
        alias_records=[
            {"id": None, "alias": alias},
        ],
    )

    assert schema.alias_records == []


def test_create_schema_strips_alias():
    schema = schemas.CreateSchema(
        name="講談社",
        yomigana="こうだんしゃ",
        alias_records=[
            {"id": None, "alias": "  Kodansha  "},
        ],
    )

    assert schema.alias_records[0].alias == "Kodansha"


def test_create_schema_converts_alias_to_string():
    schema = schemas.CreateSchema(
        name="講談社",
        yomigana="こうだんしゃ",
        alias_records=[
            {"id": None, "alias": 123},
        ],
    )

    assert schema.alias_records[0].alias == "123"


def test_create_schema_removes_empty_alias_records_and_keeps_valid_records():
    schema = schemas.CreateSchema(
        name="講談社",
        yomigana="こうだんしゃ",
        alias_records=[
            {"id": None, "alias": "Kodansha"},
            {"id": None, "alias": ""},
            {"id": None, "alias": "  "},
            {"id": None, "alias": "Kodansha-Kai"},
        ],
    )

    assert [record.alias for record in schema.alias_records] == [
        "Kodansha",
        "Kodansha-Kai",
    ]


# =========================
# Model
# =========================

@pytest.fixture
def publisher(session):
    publisher = Publisher(
        name="講談社",
        yomigana="こうだんしゃ",
    )
    session.add(publisher)

    alias = PublisherAlias(
        alias="Kodansha",
        publisher=publisher,
    )
    session.add(alias)

    session.flush()

    return publisher


def test_publisher_insert_success(session):
    publisher = Publisher(name="hoge")

    session.add(publisher)
    session.commit()

    assert publisher.id is not None


def test_publisher_insert_empty_name_fails(session):
    with pytest.raises(DomainValidationError):
        Publisher(name="")


def test_publisher_insert_space_only_name_fails(session):
    with pytest.raises(DomainValidationError):
        Publisher(name="    ")


@pytest.mark.parametrize(
    "yomigana",
    ["", "   ", None],
)
def test_publisher_normalizes_empty_yomigana(session, yomigana):
    publisher = Publisher(
        name="ほげ",
        yomigana=yomigana,
    )

    assert publisher.yomigana is None


def test_publisher_normalizes_yomigana(session):
    publisher = Publisher(
        name="ほげ",
        yomigana="  ほげ  ",
    )

    assert publisher.yomigana == "ほげ"


# =========================
# Repository
# =========================

def test_create_repository(publisher_create, session):
    publisher = repository.create(session, publisher_create)

    assert publisher.id is not None
    assert publisher.name == "講談社"
    assert publisher.yomigana == "こうだんしゃ"
    assert len(publisher.aliases) == 1
    assert publisher.aliases[0].alias == "Kodansha"


def test_update_repository(publisher, session):
    current = schemas.to_publisher_response_schema(publisher)

    current.yomigana = "こうだんしゃかい"
    current.alias_records[0].alias = "Kodansha-Kai"

    updated = repository.update(
        session,
        publisher.id,
        current,
    )

    assert updated.yomigana == "こうだんしゃかい"
    assert len(updated.aliases) == 1
    assert updated.aliases[0].alias == "Kodansha-Kai"


# =========================
# Database
# =========================

def test_no_publisher(session):
    publishers = session.execute(
        select(Publisher)
    ).scalars().all()

    assert len(publishers) == 0

