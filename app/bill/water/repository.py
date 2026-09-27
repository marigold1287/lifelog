from .models import WaterBill
from app.bill.base_repository import BaseBillRepository

class WaterBillRepository(BaseBillRepository[WaterBill]):
    model = WaterBill

repo = WaterBillRepository()