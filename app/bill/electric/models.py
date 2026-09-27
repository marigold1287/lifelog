from app.db import Base
from app.bill.base_model import BaseMixin

class ElectricBill(BaseMixin, Base):
    __tablename__ = "electric_bill"
