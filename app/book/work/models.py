from app.db import Base, validate_non_empty_string, normalize_value
from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from sqlalchemy import ForeignKey, PrimaryKeyConstraint

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

    @validates("title")
    def validate_title(self, key, name):
        return validate_non_empty_string(name, "タイトル")

    @validates("yomigana")
    def validate_yomigana(self, key, yomigana):
        return normalize_value(yomigana)

class WorkAuthor(Base):
    __tablename__ = "work_author"
    work_id: Mapped[int] = mapped_column(ForeignKey("work.id"))
    author_id: Mapped[int] = mapped_column(ForeignKey("author.id"))
    role: Mapped[str | None] = mapped_column()

    __table_args__ = (
        PrimaryKeyConstraint("work_id", "author_id"),
    )

    work: Mapped["Work"] = relationship(back_populates="work_authors")
    author: Mapped["Author"] = relationship(back_populates="work_authors")
