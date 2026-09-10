from app.book.work.schemas import PublisherSchema, AuthorSchema
from pydantic import BaseModel, ConfigDict, Field, field_validator
from datetime import date

class ResponseSchema(BaseModel):
    work_id: int
    title: str
    publisher_record: PublisherSchema
    label: str
    author_records: list[AuthorSchema]
    subtitle: str | None
    volume: str | None
    registration_date: date
    read_date: date | None
