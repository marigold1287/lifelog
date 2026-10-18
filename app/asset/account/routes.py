from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db import get_session
from .schemas import ResponseSchema, InputSchema
from app.asset.models import AccountType
from . import repository as repo


router = APIRouter(prefix="/api/account")

@router.get("/parent", response_model=list[ResponseSchema])
def get_parent_list(session: Session = Depends(get_session)):
    return repo.get_parent_list(session)

@router.get("/leaf", response_model=list[ResponseSchema])
def get_leaf(session: Session = Depends(get_session)):
    return repo.get_leaf_accounts(session)

@router.get("/type-list", response_model=list[str])
def get_type_list():
    return [a.value for a in AccountType]

@router.get("/parent/exclude/{key}", response_model=list[ResponseSchema])
def get_parent_list_exclude_me(key: int, session: Session = Depends(get_session)):
    return repo.get_parent_list(session, key)

@router.get("", response_model=list[ResponseSchema])
def get_list(session: Session = Depends(get_session)):
    return repo.get_list(session)

@router.get("/{key}", response_model=ResponseSchema)
def get(key: int, session: Session = Depends(get_session)):
    return repo.get(session, key)

@router.post("", response_model=ResponseSchema)
def create(data: InputSchema, session: Session = Depends(get_session)):
    return repo.create(session, data)

@router.put("/{key}", response_model=ResponseSchema)
def update(key: int, data: InputSchema, session: Session = Depends(get_session)):
    return repo.update(session, key, data)

@router.delete("/{key}", status_code=status.HTTP_204_NO_CONTENT)
def delete(key: int, session: Session = Depends(get_session)):
    return repo.delete(session, key)




