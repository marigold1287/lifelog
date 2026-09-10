import pytest
from app.db import Base
from app.create_tables import create_tables
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os

@pytest.fixture(scope="session")
def engine():

    DATABASE_URL = os.getenv("TEST_DATABASE_URI")

    if DATABASE_URL is None:
        raise ValueError(".envファイルでDATABASE_URIを指定してください")

    engine = create_engine(
        DATABASE_URL
    )

    yield engine

    engine.dispose()

@pytest.fixture(scope="session")
def db(engine):
    create_tables(engine)
    print("TABLES_CREATED")
    yield
    Base.metadata.drop_all(engine)
    print("TABLES_DELETED")


@pytest.fixture
def session(db, engine):
    connection = engine.connect()
    transaction = connection.begin()

    session = Session(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()