from pydantic import BaseModel, ConfigDict, Field, field_validator
from app.book.schemas import AliasRecord, AliasValidatorMixin, normalize_records
from app.db import validate_non_empty_string, DomainValidationError, normalize_value
from .models import PublisherAlias, Publisher, Label

class BaseSchema(BaseModel):
    name: str
    yomigana: str | None = None
    alias_records: list["AliasRecord"] = Field(default_factory=list)
    label_records: list["LabelRecord"] = Field(default_factory=list)

class LabelRecord(BaseModel):
    id: int | None = None
    name: str

class ValidatorMixin:
    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        try:
            return validate_non_empty_string(value, "出版社名")
        except DomainValidationError as e:
            raise ValueError(str(e)) from e

    @field_validator("yomigana")
    @classmethod
    def normalize_yomigana(cls, value: str | None) -> str | None:
        return normalize_value(value)
    
    @field_validator("label_records", mode="before")
    @classmethod
    def normalize_label_records(cls, value):
        return normalize_records(value, "name")

class CreateSchema(AliasValidatorMixin, ValidatorMixin, BaseSchema):
    pass

class ResponseSchema(BaseSchema):
    id: int

class UpdateSchema(AliasValidatorMixin, ValidatorMixin, BaseSchema):
    name: str
    yomigana: str | None
    alias_records: list[AliasRecord]
    label_records: list[LabelRecord]


def to_alias_schema(alias: PublisherAlias) -> AliasRecord:
    return AliasRecord(
        id=alias.id,
        alias=alias.alias,
    )

def to_label_schema(label: Label) -> LabelRecord:
    return LabelRecord(
        id=label.id,
        name=label.name,
    )

def to_publisher_response_schema(publisher: Publisher) -> ResponseSchema:
    alias_records = [
        to_alias_schema(alias)
        for alias in publisher.aliases
    ]
    label_records = [
        to_label_schema(label)
        for label in publisher.labels
    ]

    return ResponseSchema(
        id=publisher.id,
        name=publisher.name,
        yomigana=publisher.yomigana,
        alias_records=alias_records,
        label_records=label_records,
    )