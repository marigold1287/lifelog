from app.db import Base, validate_non_empty_string
from typing import List, TYPE_CHECKING
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

if TYPE_CHECKING:
    from app.book.work import Work

class Publisher(Base):
    __tablename__ = "publisher"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    yomigana: Mapped[str | None] = mapped_column()

    aliases: Mapped[List["PublisherAlias"]] = relationship(
        back_populates="publisher",
        cascade="all, delete-orphan",
    )
    labels: Mapped[List["Label"]] = relationship(
        back_populates="publisher",
        cascade="all, delete-orphan",
    )

    @property
    def works(self):
        return [work for label in self.labels for work in label.works]

    @property
    def work_records(self):
        return [
            work.work_record
            for work in self.works
        ]

    @validates("name")
    def validate_name(self, key, name):
        return validate_non_empty_string(name, "出版社名")

    @property
    def publisher_record(self):
        return {
            "id": self.id,
            "name": self.name,
            "yomigana": self.yomigana,
            "alias_records": self.alias_records,
            "label_records": self.label_records,
        }

    @property
    def label_records(self) -> list[dict]:
        return [
            label.label_record
            for label in self.labels
        ]

    @property
    def alias_records(self) -> list[dict]:
        return [
            alias.alias_record
            for alias in self.aliases
        ]

class Label(Base):
    __tablename__ = "label"
    id: Mapped[int] = mapped_column(primary_key=True)
    publisher_id: Mapped[int] = mapped_column(ForeignKey("publisher.id"))
    name: Mapped[str] = mapped_column()

    publisher: Mapped["Publisher"] = relationship(back_populates="labels")
    works: Mapped[List["Work"]] = relationship(back_populates="label")

    __table_args__ = (
        UniqueConstraint("publisher_id", "name", name="uq_publisher_label_name"),
    )

    @validates("name")
    def validate_alias(self, key, alias):
        return validate_non_empty_string(alias, "レーベル名")

    @property
    def label_record(self):
        return {
            "id": self.id,
            "name": self.name,
        }

    
class PublisherAlias(Base):
    __tablename__ = "publisher_alias"
    id: Mapped[int] = mapped_column(primary_key=True)
    publisher_id: Mapped[int] = mapped_column(ForeignKey("publisher.id"))
    alias: Mapped[str] = mapped_column()

    publisher: Mapped["Publisher"] = relationship(back_populates="aliases")

    @validates("alias")
    def validate_alias(self, key, alias):
        return validate_non_empty_string(alias, "エイリアス")

    @property
    def alias_record(self):
        return {
            "id": self.id,
            "alias": self.alias,
        }