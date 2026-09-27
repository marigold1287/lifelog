from pydantic import BaseModel, field_validator
from datetime import date
from app.db import normalize_value
from .models import Book

class ResponseSchema(BaseModel):
    work_id: int
    title: str
    yomigana: str | None
    publisher_id: int
    label_id: int
    author_ids: list[int]
    subtitle: str | None
    volume: str | None
    registration_date: date
    read_date: date | None

class ReadDateSchema(BaseModel):
    id: int | None
    read_date: date | None

class BookInputSchema(BaseModel):
    id: int | None
    title: str | None
    volume: str | None
    isbn: str | None
    amazon_asin: str | None
    registration_date: date
    read_dates: list[ReadDateSchema]

    @field_validator("isbn")
    @classmethod
    def validate_isbn(cls, value: str | None) -> str | None:
        if value is None or not value.strip():
            return None

        return value.strip().replace("-", "").replace("ー", "")

    @field_validator("amazon_asin")
    @classmethod
    def validate_amazon_asin(cls, value: str | None) -> str | None:
        return normalize_value(value)


def to_input_schema(book: Book) -> BookInputSchema:
    read_dates = [
        ReadDateSchema(
            id=reading.id,
            read_date=reading.read_date,
        )
        for reading in book.readings
    ]

    return BookInputSchema(
        id=book.id,
        title=book.title,
        volume=book.volume,
        isbn=book.isbn,
        amazon_asin=book.amazon_asin,
        registration_date=book.registration_date,
        read_dates=read_dates
    )


def to_response_schema(book: Book) -> list[ResponseSchema]:
    base = {
        "work_id": book.work.id,
        "title": book.work.title,
        "yomigana": book.work.yomigana,
        "publisher_id": book.work.label.publisher_id,
        "label_id": book.work.label_id,
        "author_ids": [
            work_author.author_id
            for work_author in book.work.work_authors
        ],
        "subtitle": book.title,
        "volume": book.volume,
        "registration_date": book.registration_date,
    }

    if not book.readings:
        return [
            ResponseSchema(
                **base,
                read_date=None,
            )
        ]

    return [
        ResponseSchema(
            **base,
            read_date=reading.read_date,
        )
        for reading in book.readings
    ]