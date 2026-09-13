from pydantic import BaseModel, ConfigDict, Field, field_validator
from app.book.work.schemas import WorkSchema
from app.book.schemas import AliasRecord, AliasValidatorMixin
from app.db import validate_non_empty_string, DomainValidationError

class ValidatorMixin:
    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        try:
            return validate_non_empty_string(value, "著者名")
        except DomainValidationError as e:
            raise ValueError(str(e)) from e



class BaseSchema(BaseModel):
    name: str
    yomigana: str | None = None
    note: str | None = None
    alias_records: list[AliasRecord] = Field(default_factory=list)


class CreateSchema(ValidatorMixin, AliasValidatorMixin, BaseSchema):
    pass

class ResponseSchema(BaseSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)


class ResponseDetailSchema(BaseSchema):
    id: int
    work_records: list["WorkSchema"]

    model_config = ConfigDict(from_attributes=True)

class UpdateSchema(ValidatorMixin, AliasValidatorMixin, BaseSchema):
    name: str | None = None
    yomigana: str | None = None
    note: str | None = None
    alias_records: list[AliasRecord] | None = None

    model_config = ConfigDict(from_attributes=True)
