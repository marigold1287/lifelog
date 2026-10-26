from fastapi import APIRouter, Depends, Query
from typing import Annotated
from sqlalchemy.orm import Session
from app.db import get_session
from .schemas import AssetResponseSchema
from .account import account_router
from .holding import holding_router
from .transaction import transaction_router
from .price import price_router
from .repository import AssetRepository, KakeiboRepository
from datetime import date

router = APIRouter()

asset_router = APIRouter(prefix="/api/asset")

router.include_router(asset_router)
router.include_router(account_router)
router.include_router(holding_router)
router.include_router(transaction_router)
router.include_router(price_router)


# from .services import get_wide

# @asset_router.get("", response_model=list[AssetResponseSchema])
# def get_daily_by_category(session: Session = Depends(get_session)):
#     return get_wide(session)


@asset_router.get("", response_model=list[AssetResponseSchema])
def get_daily_by_category(session: Session = Depends(get_session)):
    repo = AssetRepository(session)
    return repo.get_history(date(2016, 4, 1), date.today())



@asset_router.get("/kakeibo")
def get_statistics(
    year: Annotated[int, Query(ge=1900, le=2100)],
    month: Annotated[int | None, Query(ge=1, le=12)] = None,
    session: Session = Depends(get_session), 
):
    repo = KakeiboRepository(session)

    return repo.get_statistics(year, month)



@asset_router.get("/kakeibo/entry")
def get_entries(
    year: Annotated[int | None, Query(ge=1900, le=2100)] = None,
    month: Annotated[int | None, Query(ge=1, le=12)] = None,
    session: Session = Depends(get_session), 
):
    repo = KakeiboRepository(session)

    return repo.get_entries(year, month)