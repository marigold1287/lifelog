from app.db import Base, validate_non_empty_string
from typing import List
from datetime import date
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from sqlalchemy import ForeignKey, PrimaryKeyConstraint, UniqueConstraint

from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from app.book.publisher import Label
    from app.book.author import Author
    from app.book.book import Book

def volume_sort_key(book):
    try:
        return (0, float(book.volume))
    except (TypeError, ValueError):
        return (1, book.volume or "")

class Work(Base):
    __tablename__ = "work"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column()
    yomigana: Mapped[str | None] = mapped_column()
    label_id: Mapped[int] = mapped_column(ForeignKey("label.id"))

    label: Mapped["Label"] = relationship(back_populates="works")
    books: Mapped[List["Book"]] = relationship(back_populates="work", cascade="all, delete-orphan")
    work_authors: Mapped[List["WorkAuthor"]] = relationship(
        back_populates="work",
        cascade="all, delete-orphan",
    )

    @property
    def publisher(self):
        return self.label.publisher

    @property
    def authors(self):
        return ", ".join([work_author.author.name for work_author in self.work_authors])

    @property
    def book_records(self):
        return [
            book.book_record
            for book in sorted(self.books, key=volume_sort_key)
        ]

    @property
    def work_record(self):
        return {
            "id": self.id,
            "publisher_record": self.publisher.publisher_record,
            "yomigana": self.yomigana,
            # "publisher": self.label.publisher.name,
            # "publisher_aliases": [alias.alias for alias in self.publisher.aliases],
            # "publisher_yomigana": self.publisher.yomigana,
            # "publisher_id": self.label.publisher_id,
            "authors": self.authors,
            "label_id": self.label_id,
            "label": self.label.name,
            "title": self.title,
            "author_records": self.author_records,
        }

    @property
    def work_detail_record(self):
        return {
            "book_records": self.book_records,
            **self.work_record,
        }
    

    @property
    def author_records(self):
        return [
            {
                **work_author.author.author_record,
                "role": work_author.role,
            }
            for work_author in self.work_authors
        ]

class WorkAuthor(Base):
    __tablename__ = "work_author"
    work_id: Mapped[int] = mapped_column(ForeignKey("work.id"))
    author_id: Mapped[int] = mapped_column(ForeignKey("author.id"))
    role: Mapped[str | None] = mapped_column()

    __table_args__ = (
        PrimaryKeyConstraint("work_id", "author_id"),
    )

    work: Mapped["Work"] = relationship(back_populates="work_authors")
    author: Mapped["Author"] = relationship(back_populates="works")
