from app.db import Base
from app.bill.base_model import BaseMixin

class GasBill(BaseMixin, Base):
    __tablename__ = "gas_bill"
