from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
import datetime
from app.db import Base
from app.asset.models import Entry

class DonationDeduction(Base):
    __tablename__ = "donation_deduction"

    entry_id: Mapped[int] = mapped_column(ForeignKey("entry.id"), primary_key=True)
    is_shimin_zei_deduction: Mapped[bool] = mapped_column()
    is_kenmin_zei_deduction: Mapped[bool] = mapped_column()
    is_shotoku_zei_deduction: Mapped[bool] = mapped_column()
    deduction_year: Mapped[int] = mapped_column()

    entry: Mapped[Entry] = relationship()