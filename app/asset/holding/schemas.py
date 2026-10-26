from pydantic import BaseModel, ConfigDict, Field, field_validator
from app.db import validate_non_empty_string, DomainValidationError, normalize_value
import datetime as dt
from app.asset.models import HoldingType

class ResponseSchema(BaseModel):
    id: int
    name: str
    type: HoldingType
    symbol: str | None
    total_quantity: int
    acquisition_cost: float
    current_value: float | None
    profit_loss: float | None
    profit_loss_rate: float | None
    price_per_units: int


class InputSchema(BaseModel):
    name: str
    type: HoldingType
    symbol: str | None
    currency: str
    price_source: str | None
    price_per_units: int

class ResponseDetailSchema(BaseModel):
    id: int
    name: str
    type: HoldingType
    symbol: str | None
    currency: str
    price_source: str | None
    price_per_units: int
    current_unit_price: float | None
    entries: list["EntrySchema"]


class EntrySchema(BaseModel):
    account: str
    total_quantity: float
    average_unit_price: float
    acquisition_cost: float
    current_value: float | None
    profit_loss: float | None
    profit_loss_rate: float | None

class PriceSchema(BaseModel):
    date: dt.date
    price: float

