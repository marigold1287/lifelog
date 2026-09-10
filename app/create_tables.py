from app.db import Base, engine
from app.book.models import (
    Work, Book, WorkAuthor,
    Author,
    Publisher, PublisherAlias, Label
)

def create_tables(engine):
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    create_tables(engine)