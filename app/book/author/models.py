from app.db import Base, validate_non_empty_string, normalize_value
from typing import List, TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from sqlalchemy import ForeignKey

if TYPE_CHECKING:
    from app.book.work import WorkAuthor


class Author(Base):
    __tablename__ = "author"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    yomigana: Mapped[str | None] = mapped_column()
    note: Mapped[str | None] = mapped_column()

    aliases: Mapped[List["AuthorAlias"]] = relationship(
        back_populates="author",
        cascade="all, delete-orphan",
    )

    work_authors: Mapped[List["WorkAuthor"]] = relationship(
        back_populates="author",
        cascade="all, delete-orphan",
    )

    @validates("name")
    def validate_name(self, key, value):
        return validate_non_empty_string(value, "著者名")

    @validates("yomigana")
    def validate_yomigana(self, key, value):
        return normalize_value(value)

    @validates("note")
    def validate_note(self, key, value):
        return normalize_value(value)

class AuthorAlias(Base):
    __tablename__ = "author_alias"
    id: Mapped[int] = mapped_column(primary_key=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("author.id"))
    alias: Mapped[str] = mapped_column()

    author: Mapped["Author"] = relationship(back_populates="aliases")

    @validates("alias")
    def validate_alias(self, key, alias):
        return validate_non_empty_string(alias, "エイリアス")