from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db import get_session
from app.asset.price.repository import get_latest_prices, get_latest_price
from .schemas import ResponseSchema, InputSchema, ResponseDetailSchema
from .services import to_detail_schema, to_list_response_schema
from . import repository as repo

router = APIRouter(prefix="/api/holding")

@router.get("", response_model=list[ResponseSchema])
def get_list(session: Session = Depends(get_session)):

    price_map = get_latest_prices(session)
    
    return [
        to_list_response_schema(holding, price_map.get(holding.id, None))
        for holding in repo.get_list(session)
    ]

@router.get("/{key}", response_model=ResponseDetailSchema)
def get(key: int, session: Session = Depends(get_session)):
    latest_price = get_latest_price(session, key)
    return to_detail_schema(repo.get(session, key), latest_price)

@router.post("", response_model=ResponseDetailSchema)
def create(data: InputSchema, session: Session = Depends(get_session)):
    return to_detail_schema(repo.create(session, data), None)

@router.put("/{key}", response_model=ResponseDetailSchema)
def update(key: int, data: InputSchema, session: Session = Depends(get_session)):
    return to_detail_schema(repo.update(session, key, data), None)

@router.delete("/{key}", status_code=status.HTTP_204_NO_CONTENT)
def delete(key: int, session: Session = Depends(get_session)):
    return repo.delete(session, key)




