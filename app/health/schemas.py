from pydantic import BaseModel, ConfigDict, field_validator
from app.db import DomainValidationError, validate_non_empty_string
import datetime

class ValidatorMixin:
    pass

        
class CreateSchema(ValidatorMixin, BaseModel):
    date: datetime.date


    height: float | None
    weight: float | None
    waist: float | None

    systolic_bp: int | None
    diastolic_bp: int | None

    vision_right: float | None
    vision_left: float | None
    hearing_right: str | None
    hearing_left: str | None

    # 尿検査
    urinalysis: str | None

    # 血液検査（貧血・血球）
    rbc: int | None
    hemoglobin: float | None    # ヘモグロビン (g/dL)
    wbc: int | None
    hematocrit: float | None    # ヘマトクリット (%)
    platelets: float | None     # 血小板数 (万/μL)
    esr: float | None           # 赤沈 (mm/h)

    # 脂質
    hdl_cholesterol: float | None  # HDL (mg/dL)
    ldl_cholesterol: float | None  # LDL (mg/dL)
    triglycerides: float | None    # 中性脂肪 (mg/dL)

    # 糖代謝
    blood_glucose: float | None    # 血糖 (mg/dL)
    hba1c: float | None            # HbA1c (%)

    # 肝機能
    ast: float | None           # AST (U/L)
    alt: float | None           # ALT (U/L)
    gamma_gtp: float | None     # γ-GTP (U/L)

    # 心電図
    ecg: str | None                 # 心電図（所見）

    note: str | None                       # 備考


class ResponseSchema(BaseModel):
    id: int
    date: datetime.date

    height: float | None
    weight: float | None
    waist: float | None
    bmi: float | None

    systolic_bp: int | None
    diastolic_bp: int | None

    vision_right: float | None
    vision_left: float | None
    hearing_right: str | None
    hearing_left: str | None

    # 尿検査
    urinalysis: str | None

    # 血液検査（貧血・血球）
    rbc: int | None
    hemoglobin: float | None    # ヘモグロビン (g/dL)
    wbc: int | None
    hematocrit: float | None    # ヘマトクリット (%)
    platelets: float | None     # 血小板数 (万/μL)
    esr: float | None           # 赤沈 (mm/h)

    # 脂質
    hdl_cholesterol: float | None  # HDL (mg/dL)
    ldl_cholesterol: float | None  # LDL (mg/dL)
    triglycerides: float | None    # 中性脂肪 (mg/dL)

    # 糖代謝
    blood_glucose: float | None    # 血糖 (mg/dL)
    hba1c: float | None            # HbA1c (%)

    # 肝機能
    ast: float | None           # AST (U/L)
    alt: float | None           # ALT (U/L)
    gamma_gtp: float | None     # γ-GTP (U/L)

    # 心電図
    ecg: str | None                 # 心電図（所見）

    note: str | None                       # 備考

    model_config = ConfigDict(from_attributes=True)

class UpdateSchema(CreateSchema):
    model_config = ConfigDict(from_attributes=True)
