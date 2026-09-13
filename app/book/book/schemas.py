from app.book.work.schemas import PublisherSchema, AuthorSchema
from pydantic import BaseModel, ConfigDict, Field, field_validator
from datetime import date

class ResponseSchema(BaseModel):
    work_id: int
    title: str
    yomigana: str | None
    publisher_id: int
    label_id: int
    author_ids: list[int]
    label: str
    subtitle: str | None
    volume: str | None
    registration_date: date
    read_date: date | None
