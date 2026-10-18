from pydantic import BaseModel, ConfigDict, Field, field_validator, PlainSerializer
from decimal import Decimal
from typing import Annotated
from app.db import validate_non_empty_string, DomainValidationError, normalize_value
import datetime as dt
from app.asset.models import HoldingType, TxType

Qty = Annotated[
    Decimal,
    Field(max_digits=20, decimal_places=6),
    PlainSerializer(float, return_type=float, when_used="json"),
]

class TransactionViewResponseSchema(BaseModel):
    id: int
    trade_date: dt.date
    type: TxType
    shop: str | None
    note: str | None

class TransactionResponseSchema(BaseModel):
    id: int
    trade_date: dt.date
    type: TxType
    shop: str | None
    note: str | None
    entries: list["EntryResponseSchema"]

class EntryResponseSchema(BaseModel):
    id: int
    account_id: int
    holding_id: int
    quantity: Qty
    unit_price: Qty | None = None
    item_name: str | None = Field(default=None, max_length=200)
    memo: str | None = Field(default=None, max_length=500)


class InputSchema(BaseModel):
    trade_date: dt.date
    type: TxType
    shop: str | None
    note: str | None
    entries: list["EntryInputSchema"]

class EntryInputSchema(BaseModel):
    id: int | None = None
    account_id: int
    holding_id: int
    quantity: Qty
    unit_price: Qty | None = None
    item_name: str | None = Field(default=None, max_length=200)
    memo: str | None = Field(default=None, max_length=500)