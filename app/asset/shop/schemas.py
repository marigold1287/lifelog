from pydantic import BaseModel, ConfigDict, Field, field_validator, PlainSerializer
from decimal import Decimal
from typing import Annotated
from app.db import validate_non_empty_string, DomainValidationError, normalize_value
import datetime as dt
from app.asset.models import HoldingType, TxType
from app.asset.models import Shop
from .services import label_of

class ListResponseSchema(BaseModel):
    id: int
    name: str
    label: str


def to_list_response_schema(shop: Shop, mapping: dict[int, Shop]) -> ListResponseSchema:
    label = label_of(shop, mapping)

    return ListResponseSchema(
        id=shop.id,
        name=shop.name,
        label=label
    )

