from app.db import Base, validate_non_empty_string
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

    works: Mapped[List["WorkAuthor"]] = relationship(
        back_populates="author",
        cascade="all, delete-orphan",
    )

    @property
    def work_records(self):
        return [
            work_author.work.work_record
            for work_author in self.works
        ]
    
    @property
    def alias_records(self) -> list[dict]:
        return [
            alias.alias_record
            for alias in self.aliases
        ]

    @property
    def author_record(self):
        return {
            "id": self.id,
            "name": self.name,
            "yomigana": self.yomigana,
            "note": self.note,
            "alias_records": self.alias_records,
        }


class AuthorAlias(Base):
    __tablename__ = "author_alias"
    id: Mapped[int] = mapped_column(primary_key=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("author.id"))
    alias: Mapped[str] = mapped_column()

    author: Mapped["Author"] = relationship(back_populates="aliases")

    @validates("alias")
    def validate_alias(self, key, alias):
        return validate_non_empty_string(alias, "エイリアス")

    @property
    def alias_record(self):
        return {
            "id": self.id,
            "alias": self.alias,
        }