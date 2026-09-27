from pydantic import BaseModel, ConfigDict,  field_validator
from app.db import validate_non_empty_string, DomainValidationError, normalize_value
from app.book.schemas import normalize_records
from .models import Work
from app.book.book.schemas import (
    to_input_schema as to_book_input_schema,
    BookInputSchema,
)

class AuthorSchema(BaseModel):
    id: int | None
    name: str
    role: str | None

class ValidatorMixin:
    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        try:
            return validate_non_empty_string(value, "タイトル")
        except DomainValidationError as e:
            raise ValueError(str(e)) from e

    @field_validator("yomigana")
    @classmethod
    def validate_yomigana(cls, value: str | None) -> str | None:
        return normalize_value(value)

    @field_validator("publisher")
    @classmethod
    def validate_publisher(cls, value: str) -> str:
        try:
            return validate_non_empty_string(value, "出版社名")
        except DomainValidationError as e:
            raise ValueError(str(e)) from e

    @field_validator("label")
    @classmethod
    def validate_label(cls, value: str) -> str:
        try:
            return validate_non_empty_string(value, "レーベル名")
        except DomainValidationError as e:
            raise ValueError(str(e)) from e

    @field_validator("author_records", mode="before")
    @classmethod
    def normalize_author_records(cls, value):
        return normalize_records(value, "name")

class InputResponseSchema(BaseModel):
    title: str
    yomigana: str | None
    publisher: str
    publisher_id: int | None
    label: str
    label_id: int | None
    author_records: list[AuthorSchema]
    book_records: list[BookInputSchema]


class InputSchema(ValidatorMixin, InputResponseSchema):
    pass

class ResponseSchema(BaseModel):
    id: int
    title: str
    yomigana: str | None
    publisher_id: int
    label_id: int
    author_ids: list[int]

def to_response_schema(work: Work) -> ResponseSchema:
    return ResponseSchema(
        id=work.id,
        title=work.title,
        yomigana=work.yomigana,
        publisher_id=work.label.publisher_id,
        label_id=work.label_id,
        author_ids=[author.author_id for author in work.work_authors],
    )


def to_input_schema(work: Work) -> InputResponseSchema:
    author_records = [
        AuthorSchema(
            id=work_author.author_id,
            name=work_author.author.name,
            role=work_author.role,
        )
        for work_author in work.work_authors
    ]
    book_records = [
        to_book_input_schema(book)
        for book in work.books
    ]

    return InputResponseSchema(
        title=work.title,
        yomigana=work.yomigana,
        publisher=work.publisher.name,
        publisher_id=work.label.publisher_id,
        label=work.label.name,
        label_id=work.label_id,
        author_records=author_records,
        book_records=book_records,
    )