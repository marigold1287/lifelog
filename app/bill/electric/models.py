from app.db import Base, validate_non_empty_string
from typing import List, TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from sqlalchemy import ForeignKey
import datetime

class ElectricBill(Base):
    __tablename__ = "electric_bill"

    id: Mapped[int] = mapped_column(primary_key=True)
    start_date: Mapped[datetime.date] = mapped_column(unique=True)
    end_date: Mapped[datetime.date] = mapped_column(unique=True)
    total: Mapped[int] = mapped_column()
    usage: Mapped[float] = mapped_column()
    provider: Mapped[str] = mapped_column()

    @property
    def unit_price(self) -> int | None:
        if self.usage == 0:
            return None
        return round(self.total / self.usage)

    @property
    def daily_cost(self) -> int | None:
        days = (self.end_date - self.start_date).days + 1

        return round(self.total / days)