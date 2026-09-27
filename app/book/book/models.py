from app.db import Base, normalize_value
from typing import List
from datetime import date
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from sqlalchemy import ForeignKey

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

    @validates("title")
    def validate_title(self, key, title):
        return normalize_value(title)

    @validates("volume")
    def validate_volume(self, key, volume):
        return normalize_value(volume)

    @validates("isbn")
    def validate_isbn(self, key, isbn: str | None):
        isbn = normalize_value(isbn)
        if isbn is None:
            return None

        return isbn.strip().replace("-", "").replace("ー", "")

    @validates("amazon_asin")
    def validate_amazon_asin(self, key, amazon_asin: str | None):
        return normalize_value(amazon_asin)
    
class BookReading(Base):
    __tablename__ = "book_reading"

    id: Mapped[int] = mapped_column(primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("book.id"))
    read_date: Mapped[date] = mapped_column()

    book: Mapped["Book"] = relationship(back_populates="readings")
