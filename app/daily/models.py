from sqlalchemy.orm import Mapped, mapped_column
import datetime
from app.db import Base

class Daily(Base):
    __tablename__ = "daily"

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[datetime.date] = mapped_column(unique=True)

    weight: Mapped[float | None] = mapped_column()
    room_temperature: Mapped[float | None] = mapped_column()
    room_humidity: Mapped[float | None] = mapped_column()
    body_temperature: Mapped[float | None] = mapped_column()

