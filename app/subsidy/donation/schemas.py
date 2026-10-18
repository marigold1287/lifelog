from pydantic import BaseModel, ConfigDict, field_validator
from app.db import DomainValidationError, validate_non_empty_string
from app.asset.models import Entry
from .models import DonationDeduction
import datetime

class ValidatorMixin:
    pass

class ResponseSchema(BaseModel):
    entry_id: int
    trade_date: datetime.date
    shop: str | None
    deduction_year: int
    is_shimin_zei_deduction: bool
    is_kenmin_zei_deduction: bool
    is_shotoku_zei_deduction: bool

    model_config = ConfigDict(from_attributes=True)

class CreateSchema(ValidatorMixin, BaseModel):
    entry_id: int
    deduction_year: int
    is_shimin_zei_deduction: bool
    is_kenmin_zei_deduction: bool
    is_shotoku_zei_deduction: bool

class UpdateSchema(CreateSchema):
    model_config = ConfigDict(from_attributes=True)

class CreateUpdateResponse(BaseModel):
    entry_id: int

class EntryListSchema(BaseModel):
    id: int
    date: datetime.date
    shop: str | None
    label: str

def to_entry_list_schema(entry: Entry):
    return EntryListSchema(
        id=entry.id,
        date=entry.transaction.trade_date,
        shop=entry.transaction.shop,
        label=f"{entry.transaction.trade_date}, {entry.transaction.shop}, {int(entry.quantity)}円"
    )

def to_response_schema(record: DonationDeduction):
    return ResponseSchema(
        entry_id=record.entry.id,
        trade_date=record.entry.transaction.trade_date,
        shop=record.entry.transaction.shop,
        deduction_year=record.deduction_year,
        is_shimin_zei_deduction=record.is_shimin_zei_deduction,
        is_kenmin_zei_deduction=record.is_kenmin_zei_deduction,
        is_shotoku_zei_deduction=record.is_shotoku_zei_deduction,
    )
