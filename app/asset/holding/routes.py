from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db import get_session
from app.asset.price.repository import get_latest_price
from .schemas import ResponseSchema, InputSchema, ResponseDetailSchema
from .services import to_detail_schema, to_list_response_schema
from . import repository as repo

router = APIRouter(prefix="/api/holding")

@router.get("", response_model=list[ResponseSchema])
def get_list(session: Session = Depends(get_session)):
    
    return [
        to_list_response_schema(holding, get_latest_price(session, holding.id))
        for holding in repo.get_list(session)
    ]

@router.get("/{key}", response_model=ResponseDetailSchema)
def get(key: int, session: Session = Depends(get_session)):
    latest_price = get_latest_price(session, key)
    return to_detail_schema(repo.get(session, key), latest_price)

@router.post("", response_model=ResponseSchema)
def create(data: InputSchema, session: Session = Depends(get_session)):
    return repo.create(session, data)

@router.put("/{key}", response_model=ResponseSchema)
def update(key: int, data: InputSchema, session: Session = Depends(get_session)):
    return repo.update(session, key, data)

@router.delete("/{key}", status_code=status.HTTP_204_NO_CONTENT)
def delete(key: int, session: Session = Depends(get_session)):
    return repo.delete(session, key)




