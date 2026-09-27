from .repository import repo as repository
from app.bill.router_factory import create_bill_router

router = create_bill_router(repository, "/api/bill/gas")