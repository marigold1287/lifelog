from pydantic import BaseModel, ConfigDict, Field, field_validator
from datetime import date

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
    label_records: list[LabelRecord] = []

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
    publisher_record: PublisherSchema
    label: str
    label_id: int | None
    author_records: list[AuthorSchema]

    model_config = ConfigDict(from_attributes=True)

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("タイトルは必須です")
        return value



class ResponseSchema(WorkSchema):
    pass

class ResponseDetailSchema(WorkSchema):
    book_records: list[BookEditSchema]

class UpdateSchema(ResponseDetailSchema):
    pass

class CreateSchema(ResponseDetailSchema):
    id: None
    pass
