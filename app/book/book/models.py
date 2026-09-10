from app.db import Base, validate_non_empty_string
from typing import List
from datetime import date
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from sqlalchemy import ForeignKey, PrimaryKeyConstraint, UniqueConstraint

from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from app.book.work import Work

class Book(Base):
    __tablename__ = "book"
    id: Mapped[int] = mapped_column(primary_key=True)
    work_id: Mapped[int] = mapped_column(ForeignKey("work.id"))
    title: Mapped[str | None] = mapped_column()
    volume: Mapped[str | None] = mapped_column()
    isbn: Mapped[str | None] = mapped_column()
    amazon_asin: Mapped[str | None] = mapped_column()
    registration_date: Mapped[date] = mapped_column(default=date.today)

    work: Mapped["Work"] = relationship(back_populates="books")

    readings: Mapped[List["BookReading"]] = relationship(
        back_populates="book",
        cascade="all, delete-orphan",
    )

    @property
    def latest_read_date(self):
        if not self.readings:
            return None
        return max(reading.read_date for reading in self.readings)

    @property
    def read_records(self):
        return [
            {
                "id": read_record.id,
                "read_date": read_record.read_date,
            }
            for read_record in self.readings
        ]

    @property
    def book_record(self):
        return {
            "id": self.id,
            "title": self.title,
            "volume": self.volume,
            "isbn": self.isbn,
            "amazon_asin": self.amazon_asin,
            "registration_date": self.registration_date,
            "read_records": self.read_records,
        }
    
    @property
    def book_list_records(self):
        base = {
            "work_id": self.work.id,
            "title": self.work.title,
            "publisher_record": self.work.publisher.publisher_record,
            "label": self.work.label.name,
            "author_records": self.work.author_records,
            "subtitle": self.title,
            "volume": self.volume,
            "registration_date": self.registration_date,
        }

        if not self.readings:
            return [{**base, "read_date": None}]

        return [
            {**base, "read_date": reading.read_date}
            for reading in self.readings
        ]

class BookReading(Base):
    __tablename__ = "book_reading"

    id: Mapped[int] = mapped_column(primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("book.id"))
    read_date: Mapped[date] = mapped_column()

    book: Mapped["Book"] = relationship(back_populates="readings")
