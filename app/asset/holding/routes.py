from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db import get_session
from app.asset.price.repository import get_latest_prices, get_latest_price
from .schemas import ResponseSchema, InputSchema, ResponseDetailSchema, HoldingSummarySchema, EntrySchema, AccountSummarySchema
from .services import to_list_response_schema, to_entry_schema, calculate_total
from . import repository as repo

router = APIRouter(prefix="/api/holding")

@router.get("", response_model=list[ResponseSchema])
def get_list(session: Session = Depends(get_session)):

    price_map = get_latest_prices(session)
    
    return [
        to_list_response_schema(HoldingSummarySchema(**holding_summary), price_map.get(holding_summary.id, None))
        for holding_summary in repo.get_holding_summaries(session)
    ]

@router.get("/{key}", response_model=ResponseDetailSchema)
def get(key: int, session: Session = Depends(get_session)):
    return repo.get(session, key)

@router.get("/{key}/summary", response_model=list[EntrySchema])
def get(key: int, session: Session = Depends(get_session)):
    summaries = repo.get_account_summaries(session, key)
    holding = repo.get(session, key)
    latest_price = get_latest_price(session, key)
    entries = [
        to_entry_schema(account_summary, latest_price)
        for account_summary in summaries
    ]

    total = calculate_total(summaries, holding.price_per_units, latest_price)

    return [*entries, total]

@router.post("", response_model=ResponseDetailSchema)
def create(data: InputSchema, session: Session = Depends(get_session)):
    return repo.create(session, data)

@router.put("/{key}", response_model=ResponseDetailSchema)
def update(key: int, data: InputSchema, session: Session = Depends(get_session)):
    return repo.update(session, key, data)

@router.delete("/{key}", status_code=status.HTTP_204_NO_CONTENT)
def delete(key: int, session: Session = Depends(get_session)):
    return repo.delete(session, key)




