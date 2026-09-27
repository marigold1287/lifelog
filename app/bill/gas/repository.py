from .models import GasBill
from app.bill.base_repository import BaseBillRepository

class GasBillRepository(BaseBillRepository[GasBill]):
    model = GasBill

repo = GasBillRepository()