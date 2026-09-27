from pydantic import BaseModel, ConfigDict, Field, field_validator
from app.book.schemas import AliasRecord, AliasValidatorMixin
from app.db import validate_non_empty_string, DomainValidationError, normalize_value
from .models import Author, AuthorAlias

class ValidatorMixin:
    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        try:
            return validate_non_empty_string(value, "著者名")
        except DomainValidationError as e:
            raise ValueError(str(e)) from e

    @field_validator("yomigana")
    @classmethod
    def validate_yomigana(cls, value: str | None) -> str | None:
        return normalize_value(value)

    @field_validator("note")
    @classmethod
    def validate_note(cls, value: str | None) -> str | None:
        return normalize_value(value)


class BaseSchema(BaseModel):
    name: str
    yomigana: str | None = None
    note: str | None = None
    alias_records: list[AliasRecord] = Field(default_factory=list)


class CreateSchema(ValidatorMixin, AliasValidatorMixin, BaseSchema):
    pass

class ResponseSchema(BaseSchema):
    id: int

class UpdateSchema(ValidatorMixin, AliasValidatorMixin, BaseSchema):
    name: str
    yomigana: str | None
    note: str | None
    alias_records: list[AliasRecord]

def to_alias_schema(alias: AuthorAlias) -> AliasRecord:
    return AliasRecord(
        id=alias.id,
        alias=alias.alias,
    )

def to_response_schema(author: Author) -> ResponseSchema:
    alias_records = [
        to_alias_schema(alias)
        for alias in author.aliases
    ]

    return ResponseSchema(
        id=author.id,
        name=author.name,
        yomigana=author.yomigana,
        note=author.note,
        alias_records=alias_records,
    )
