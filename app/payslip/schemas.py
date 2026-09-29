from pydantic import BaseModel, ConfigDict, field_validator
from app.db import DomainValidationError, validate_non_empty_string
import datetime

class ValidatorMixin:
    pass

        
class CreateSchema(ValidatorMixin, BaseModel):
    date: datetime.date
    honkyu: int
    noryokukyu: int
    mibunkyu: int
    shokuji_teate: int
    kenkyuin_teate: int
    tsukin_teate: int
    jutaku_teate: int
    nitto_teate: int
    kekkin_koujo: int
    jitan_kyushutsu_teate: int
    shoyo: int
    shoyo_kakyu: int
    tokubetsu_kakyu: int
    tokushu_kinmu_teate: int
    sonota_shikyu: int

    kenko_hoken: int
    kosei_nenkin: int
    koyo_hoken: int
    kodomo_shienkin: int
    shotoku_zei: int
    jumin_zei: int
    senyukaihi: int
    shokuji_dai: int
    shataku_ryo: int
    ryohi: int
    seimei_hoken: int
    sonota_kojo: int
    nencho_kabusoku: int


class ResponseSchema(BaseModel):
    id: int
    date: datetime.date
    total_shikyu: int
    total_kojo: int
    tedori: int

    model_config = ConfigDict(from_attributes=True)

class UpdateSchema(CreateSchema):
    model_config = ConfigDict(from_attributes=True)
