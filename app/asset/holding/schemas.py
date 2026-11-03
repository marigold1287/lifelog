from pydantic import BaseModel, ConfigDict, Field, field_validator
from app.db import validate_non_empty_string, DomainValidationError, normalize_value
import datetime as dt
from app.asset.models import HoldingType

class ResponseSchema(BaseModel):
    id: int
    name: str
    type: HoldingType
    symbol: str | None
    price_per_units: int
    total_quantity: int
    acquisition_cost: float
    current_value: float | None
    profit_loss: float | None
    profit_loss_rate: float | None


class HoldingSummarySchema(BaseModel):
    id: int
    name: str
    type: HoldingType
    symbol: str | None
    price_per_units: int
    total_quantity: int
    acquisition_cost: float

class AccountSummarySchema(BaseModel):
    name: str
    price_per_units: int
    total_quantity: int
    acquisition_cost: float


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


class EntrySchema(BaseModel):
    account: str
    total_quantity: float
    average_unit_price: float | None
    acquisition_cost: float
    current_value: float | None
    profit_loss: float | None
    profit_loss_rate: float | None

class PriceSchema(BaseModel):
    date: dt.date
    price: float

