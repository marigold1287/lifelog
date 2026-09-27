from app.db import Base, validate_non_empty_string, normalize_value
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

    @validates("name")
    def validate_name(self, key, name):
        return validate_non_empty_string(name, "出版社名")

    @validates("yomigana")
    def validate_yomigana(self, key, yomigana):
        return normalize_value(yomigana)

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

class PublisherAlias(Base):
    __tablename__ = "publisher_alias"
    id: Mapped[int] = mapped_column(primary_key=True)
    publisher_id: Mapped[int] = mapped_column(ForeignKey("publisher.id"))
    alias: Mapped[str] = mapped_column()

    publisher: Mapped["Publisher"] = relationship(back_populates="aliases")

    @validates("alias")
    def validate_alias(self, key, alias):
        return validate_non_empty_string(alias, "エイリアス")
