from pydantic import BaseModel, model_validator, field_validator
from app.db import validate_non_empty_string, DomainValidationError

class AliasRecord(BaseModel):
    id: int | None = None
    alias: str

    @field_validator("alias")
    @classmethod
    def validate_alias(cls, value: str) -> str:
        try:
            return validate_non_empty_string(value, "エイリアス")
        except DomainValidationError as e:
            raise ValueError(str(e)) from e

def normalize_records(records, key_name: str):
    if not isinstance(records, list):
        return records

    return [
        {**record, key_name: str(record[key_name]).strip()}
        for record in records
        if (
            isinstance(record, dict)
            and record.get(key_name) is not None
            and str(record[key_name]).strip()
        )
    ]

class AliasValidatorMixin:
    @field_validator("alias_records", mode="before")
    @classmethod
    def normalize_alias_records(cls, value):
        return normalize_records(value, "alias")
