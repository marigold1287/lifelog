from .models import ElectricBill
from app.bill.base_repository import BaseBillRepository

class ElectricBillRepository(BaseBillRepository[ElectricBill]):
    model = ElectricBill

repo = ElectricBillRepository()