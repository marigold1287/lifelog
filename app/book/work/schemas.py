from pydantic import BaseModel, ConfigDict, Field, field_validator
from datetime import date
from app.db import validate_non_empty_string, DomainValidationError

class AliasRecord(BaseModel):
    id: int | None = None
    alias: str

class LabelRecord(BaseModel):
    id: int | None = None
    name: str

class AuthorSchema(BaseModel):
    id: int | None = None
    name: str | None = None
    role: str | None = None
    yomigana: str | None = None
    alias_records: list[AliasRecord] = []


class PublisherSchema(BaseModel):
    id: int | None = None
    name: str
    yomigana: str | None = None
    alias_records: list[AliasRecord] = []
    # label_records: list[LabelRecord] = []

class BookEditSchema(BaseModel):
    id: int | None
    title: str | None
    volume: str | None
    isbn: str | None
    amazon_asin: str | None
    registration_date: date
    read_records: list["ReadDateEditSchema"]

class ReadDateEditSchema(BaseModel):
    id: int | None
    read_date: date | None


class WorkSchema(BaseModel):
    id: int
    title: str
    yomigana: str | None
    publisher_record: PublisherSchema
    label: str
    label_id: int | None
    author_records: list[AuthorSchema]

    model_config = ConfigDict(from_attributes=True)

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        try:
            return validate_non_empty_string(value, "タイトル")
        except DomainValidationError as e:
            raise ValueError(str(e)) from e

    @field_validator("publisher_record")
    @classmethod
    def validate_publisher_name(cls, value: PublisherSchema) -> PublisherSchema:
        try:
            value.name = validate_non_empty_string(value.name, "出版社名")
            return value
        except DomainValidationError as e:
            raise ValueError(str(e)) from e

    @field_validator("label")
    @classmethod
    def validate_label(cls, value: str) -> str:
        try:
            return validate_non_empty_string(value, "レーベル名")
        except DomainValidationError as e:
            raise ValueError(str(e)) from e


class ResponseSchema(WorkSchema):
    pass

class ResponseDetailSchema(WorkSchema):
    book_records: list[BookEditSchema]

class UpdateSchema(ResponseDetailSchema):
    pass

class CreateSchema(ResponseDetailSchema):
    id: None
    pass
