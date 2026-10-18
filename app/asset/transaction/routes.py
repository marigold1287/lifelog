from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db import get_session
from app.asset.models import TxType
from .schemas import TransactionViewResponseSchema, TransactionResponseSchema, InputSchema, EntryResponseSchema
from . import repository as repo

router = APIRouter(prefix="/api/transaction")

@router.get("", response_model=list[TransactionViewResponseSchema])
def get_list(session: Session = Depends(get_session)):
    return repo.get_list(session)

@router.get("/type-list", response_model=list[str])
def get_type_list():
    return [tx.value for tx in TxType]


@router.get("/entry/{key}", response_model=EntryResponseSchema)
def get_entry(key: int, session: Session = Depends(get_session)):
    return repo.get_entry(session, key)

@router.get("/{key}", response_model=TransactionResponseSchema)
def get(key: int, session: Session = Depends(get_session)):
    return repo.get(session, key)


@router.post("", response_model=TransactionResponseSchema)
def create(data: InputSchema, session: Session = Depends(get_session)):
    return repo.create(session, data)

@router.put("/{key}", response_model=TransactionResponseSchema)
def update(key: int, data: InputSchema, session: Session = Depends(get_session)):
    return repo.update(session, key, data)

@router.delete("/{key}", status_code=status.HTTP_204_NO_CONTENT)
def delete(key: int, session: Session = Depends(get_session)):
    return repo.delete(session, key)




