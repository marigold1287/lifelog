from app.db import Base
from app.bill.base_model import BaseMixin

class WaterBill(BaseMixin, Base):
    __tablename__ = "water_bill"
