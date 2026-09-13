from pydantic import BaseModel, ConfigDict, Field, field_validator
from app.book.work.schemas import WorkSchema
from app.db import DomainValidationError, validate_non_empty_string
import datetime

class ValidatorMixin:
    @field_validator("total")
    @classmethod
    def validate_total(cls, value: int) -> int:
        if value < 0:
            raise ValueError("合計金額は0以上の値を入力してください")
        
        return value
        
    @field_validator("usage")
    @classmethod
    def validate_usage(cls, value: float) -> float:
        if value < 0:
            raise ValueError("使用量は0以上の値を入力してください")

        return value

    @field_validator("provider")
    @classmethod
    def validate_usage(cls, value: str) -> str:
        try:
            return validate_non_empty_string(value, "プロバイダー名")
        except DomainValidationError as e:
            raise ValueError(str(e)) from e

        
class BaseSchema(BaseModel):
    start_date: datetime.date
    end_date: datetime.date
    total: int
    usage: float
    provider: str

class CreateSchema(ValidatorMixin, BaseSchema):
    pass

class ResponseSchema(BaseSchema):
    id: int
    daily_cost: int
    unit_price: int | None

    model_config = ConfigDict(from_attributes=True)

class ResponseDetailSchema(BaseSchema):
    daily_cost: int
    unit_price: int | None
    model_config = ConfigDict(from_attributes=True)

class UpdateSchema(ValidatorMixin, BaseSchema):
    model_config = ConfigDict(from_attributes=True)
