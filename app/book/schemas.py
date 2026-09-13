from pydantic import BaseModel, model_validator

class AliasRecord(BaseModel):
    id: int | None = None
    alias: str

class AliasValidatorMixin:
    @model_validator(mode="before")
    @classmethod
    def normalize_alias_records(cls, data: dict) -> dict:
        if not isinstance(data, dict):
            return data

        records = data.get("alias_records")
        if isinstance(records, list):
            data["alias_records"] = [
                {**record, "alias": str(record["alias"]).strip()}
                for record in records
                if isinstance(record, dict)
                and record.get("alias") is not None
                and str(record["alias"]).strip()
            ]

        return data
