from pydantic import BaseModel, ConfigDict, Field, field_validator
from app.db import validate_non_empty_string, DomainValidationError, normalize_value
import datetime as dt
from app.asset.models import AccountType

class ResponseSchema(BaseModel):
    id: int
    name: str
    type: AccountType
    currency: str
    parent_id: int | None
    sort_order: int
    label: str

class InputSchema(BaseModel):
    name: str
    type: AccountType
    currency: str
    sort_order: int
    parent_id: int | None
