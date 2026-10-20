from sqlalchemy.orm import Mapped, mapped_column
import datetime as dt
from app.db import Base

class HealthCheckup(Base):
    __tablename__ = "health_checkups"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    date: Mapped[dt.date] = mapped_column(nullable=False, unique=True)  # Date

    # 身体測定
    height: Mapped[float | None] = mapped_column()   # 身長 cm
    weight: Mapped[float | None] = mapped_column()   # 体重 kg
    waist: Mapped[float | None] = mapped_column()    # 腹囲 cm

    # 血圧
    systolic_bp: Mapped[int | None] = mapped_column()           # 最高血圧 - 129
    diastolic_bp: Mapped[int | None] = mapped_column()          # 最低血圧 - 84

    # 視力・聴力
    vision_right: Mapped[float | None] = mapped_column()  # 右視力 1.0 -
    vision_left: Mapped[float | None] = mapped_column()   # 左視力 1.0 -
    hearing_right: Mapped[str | None] = mapped_column()        # 右聴力（所見なし 等）
    hearing_left: Mapped[str | None] = mapped_column()         # 左聴力

    # 尿検査
    urinalysis: Mapped[str | None] = mapped_column()           # 尿検査（－/＋- 等）

    # 血液検査（貧血・血球）
    rbc: Mapped[int | None] = mapped_column()                     # 赤血球数 (万/μL) 400 - 539
    hemoglobin: Mapped[float | None] = mapped_column()    # ヘモグロビン (g/dL)  13.1 - 16.3
    wbc: Mapped[int | None] = mapped_column()                     # 白血球数 (/μL)  3100 - 8400
    hematocrit: Mapped[float | None] = mapped_column()    # ヘマトクリット (%)  38.5 - 48.9
    platelets: Mapped[float | None] = mapped_column()     # 血小板数 (万/μL)  14.5 - 32.9
    esr: Mapped[float | None] = mapped_column()           # 赤沈 (mm/h)  1 - 15

    # 脂質
    hdl_cholesterol: Mapped[float | None] = mapped_column()  # HDL (mg/dL)  40 -
    ldl_cholesterol: Mapped[float | None] = mapped_column()  # LDL (mg/dL)  60 - 119
    triglycerides: Mapped[float | None] = mapped_column()    # 中性脂肪 (mg/dL)  30 - 149

    # 糖代謝
    blood_glucose: Mapped[float | None] = mapped_column()    # 血糖 (mg/dL)  - 99
    hba1c: Mapped[float | None] = mapped_column()            # HbA1c (%) - 5.5

    # 肝機能
    ast: Mapped[float | None] = mapped_column()           # AST (U/L)  - 30
    alt: Mapped[float | None] = mapped_column()           # ALT (U/L)  - 30
    gamma_gtp: Mapped[float | None] = mapped_column()     # γ-GTP (U/L)  - 50

    # 心電図
    ecg: Mapped[str | None] = mapped_column()                 # 心電図（所見）

    note: Mapped[str | None] = mapped_column()                       # 備考

    @property
    def bmi(self) -> float | None:
        """BMI = 体重(kg) / 身長(m)^2。身長・体重が未入力なら None"""
        if not self.height or not self.weight:
            return None
        height_m = self.height / 100.0
        return round((self.weight / (height_m**2)) * 10.0) / 10.0

    @property
    def mchc(self) -> float | None:
        """MCHC = ヘモグロビン / ヘマトクリット * 100。平均赤血球ヘモグロビン量。赤血球1個の中のヘモグロビンの濃さ。"""
        if not self.hemoglobin or not self.hematocrit:
            return None
        return round((self.hemoglobin / self.hematocrit * 100) * 100.0) / 100.0

    @property
    def mcv(self) -> float | None:
        """MCV = ヘマトクリット (%) ÷ 赤血球数 (10⁶/μL) × 10。平均赤血球容積"""
        if not self.hematocrit or not self.rbc:
            return None
        return round((self.hematocrit / (self.rbc / 100)) * 100.0) / 100.0
    

    @property
    def mch(self) -> float | None:
        """MCH = ヘモグロビン (g/dL) ÷ 赤血球数 (10⁶/μL) × 10。平均赤血球ヘモグロビン量。赤血球に含まれるヘモグロビンの量"""
        if not self.hemoglobin or not self.rbc:
            return None
        return round((self.hemoglobin / (self.rbc / 100)) * 100.0) / 100.0