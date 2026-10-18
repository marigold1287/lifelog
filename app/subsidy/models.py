from sqlalchemy.orm import Mapped, mapped_column, relationship, foreign
from sqlalchemy import ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
import datetime
from app.db import Base
from app.asset.models import Entry
from .donation.models import DonationDeduction

class Subsidy(Base):
    __tablename__ = "subsidy"

    id: Mapped[int] = mapped_column(primary_key=True)
    year: Mapped[int] = mapped_column(unique=True)
    amount_after_salary_deductions: Mapped[int] = mapped_column()
    shotoku_zei_basic_deduction: Mapped[int] = mapped_column()
    jumin_zei_basic_deduction: Mapped[int] = mapped_column()
    shotoku_zei_fixed_deduction: Mapped[int] = mapped_column()
    jumin_zei_fixed_deduction: Mapped[int] = mapped_column()

    donations: Mapped[list["DonationDeduction"]] = relationship(
        primaryjoin=lambda: Subsidy.year == foreign(
            DonationDeduction.deduction_year
        ),
        viewonly=True,
    )