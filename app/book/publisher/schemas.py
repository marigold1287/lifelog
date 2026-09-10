from pydantic import BaseModel, ConfigDict, Field
from app.book.work.schemas import WorkSchema

class LabelRecord(BaseModel):
    id: int | None = None
    name: str

class AliasRecord(BaseModel):
    id: int | None = None
    alias: str


class BaseSchema(BaseModel):
    name: str
    yomigana: str | None = None
    alias_records: list[AliasRecord] = Field(default_factory=list)
    label_records: list[LabelRecord] = Field(default_factory=list)

class CreateSchema(BaseSchema):
    pass

class ResponseSchema(BaseSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)

class ResponseDetailSchema(BaseSchema):
    id: int
    work_records: list["WorkSchema"]

    model_config = ConfigDict(from_attributes=True)


class UpdateSchema(BaseSchema):
    name: str | None = None
    yomigana: str | None = None
    alias_records: list[AliasRecord] | None = None
    label_records: list[LabelRecord] | None = None

    model_config = ConfigDict(from_attributes=True)
