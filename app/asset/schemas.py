from pydantic import BaseModel, PlainSerializer, Field
from decimal import Decimal
from typing import Annotated
import datetime as dt


Qty = Annotated[
    Decimal,
    Field(max_digits=20, decimal_places=6),
    PlainSerializer(float, return_type=float, when_used="json"),
]


class AssetResponseSchema(BaseModel):
    date: dt.date
    cash: int
    fund: int
    pension: int
    stock: int
    total: int

class EntryResponseSchema(BaseModel):
    transaction_id: int
    transaction_type: str
    trade_date: dt.date
    shop: str | None
    note: str | None
    account: str
    account_type: str
    holding: str
    holding_type: str
    item_name: str | None
    quantity: Qty
    unit_price: Qty | None
    memo: str | None