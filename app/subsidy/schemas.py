from pydantic import BaseModel, ConfigDict, field_validator
from app.db import DomainValidationError, validate_non_empty_string
import datetime
from .models import Subsidy

class ValidatorMixin:
    pass



class ResponseSchema(BaseModel):
    id: int
    year: int
    amount_after_salary_deductions: int
    shotoku_zei_basic_deduction: int
    jumin_zei_basic_deduction: int
    shotoku_zei_fixed_deduction: int
    jumin_zei_fixed_deduction: int
    total_shimin_zei_deduction: int
    total_kenmin_zei_deduction: int
    total_shotoku_zei_deduction: int

    model_config = ConfigDict(from_attributes=True)

class CreateSchema(ValidatorMixin, BaseModel):
    year: int
    amount_after_salary_deductions: int
    shotoku_zei_basic_deduction: int
    jumin_zei_basic_deduction: int
    shotoku_zei_fixed_deduction: int
    jumin_zei_fixed_deduction: int

class UpdateSchema(CreateSchema):
    model_config = ConfigDict(from_attributes=True)

class NenmatsuChoseiSchema(BaseModel):
    nenshu: int
    shiharai_kingaku: int
    ideco: int
    shakai_hoken_deduction: int
    total_shakai_hoken_deduction: int
    seimei_hoken_deduction: float
    basic_deduction: int
    total_deduction: float
    kazei_shotoku: float
    paid_shotoku_zei: float
    shotoku_zei: float
    nenmatsu_chosei_kabusoku: float

class KakuteiShinkokuSchema(BaseModel):
    shotoku: int
    zatsu_shotoku: int
    haitou: int
    kazei_shotoku: int
    furusato: int
    shotoku_zei_donation: int
    shotoku_donation_deduction: int
    shotoku_deduction: int
    zeigaku_deduction: int

    shotoku_zei: int

    paid_shotoku_zei: int

    kanpu: int

class JuminZeiSchema(BaseModel):
    shotoku: int
    total_deduction: int
    kazei_shotoku: int
    
    shimin_zei: int
    kenmin_zei: int
    jumin_zei: int
    
    furusato_limit:int


class TaxSchema(BaseModel):
    nenmatsu_chosei: NenmatsuChoseiSchema
    kakutei_shinkoku: KakuteiShinkokuSchema
    jumin_zei: JuminZeiSchema

def to_response_schema(subsidy: Subsidy):
    total_shimin_zei_deduction = 0
    total_kenmin_zei_deduction = 0
    total_shotoku_zei_deduction = 0

    for donation in subsidy.donations:
        if donation.is_shimin_zei_deduction:
            total_shimin_zei_deduction += donation.entry.quantity
        if donation.is_kenmin_zei_deduction:
            total_kenmin_zei_deduction += donation.entry.quantity
        if donation.is_shotoku_zei_deduction:
            total_shotoku_zei_deduction += donation.entry.quantity

    return ResponseSchema(
        id=subsidy.id,
        year=subsidy.year,
        amount_after_salary_deductions=subsidy.amount_after_salary_deductions,
        shotoku_zei_basic_deduction=subsidy.shotoku_zei_basic_deduction,
        jumin_zei_basic_deduction=subsidy.jumin_zei_basic_deduction,
        shotoku_zei_fixed_deduction=subsidy.shotoku_zei_fixed_deduction,
        jumin_zei_fixed_deduction=subsidy.jumin_zei_fixed_deduction,
        total_shimin_zei_deduction=total_shimin_zei_deduction,
        total_kenmin_zei_deduction=total_kenmin_zei_deduction,
        total_shotoku_zei_deduction=total_shotoku_zei_deduction,
    )

def to_tax_response_schema(taxes: dict[int, TaxSchema]):
    return {
        "nenmatsu_chosei": [{
            "year": year, 
            **tax.nenmatsu_chosei.model_dump()
        } for year, tax  in taxes.items()] ,
        "kakutei_shinkoku": [{
            "year": year, 
            **tax.kakutei_shinkoku.model_dump()
        } for year, tax  in taxes.items()] ,
        "jumin_zei": [{
            "year": year, 
            **tax.jumin_zei.model_dump()
        } for year, tax  in taxes.items()],
    }