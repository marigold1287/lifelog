from pydantic import BaseModel, ConfigDict, field_validator
from app.db import DomainValidationError, validate_non_empty_string
import datetime

class ValidatorMixin:
    pass

        
class CreateSchema(ValidatorMixin, BaseModel):
    date: datetime.date

    weight: float | None
    room_temperature: float | None
    room_humidity: float | None
    body_temperature: float | None


class ResponseSchema(BaseModel):
    id: int
    date: datetime.date

    weight: float | None
    room_temperature: float | None
    room_humidity: float | None
    body_temperature: float | None

    model_config = ConfigDict(from_attributes=True)

class UpdateSchema(CreateSchema):
    model_config = ConfigDict(from_attributes=True)
