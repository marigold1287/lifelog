from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db import get_session
from .schemas import CreateSchema, ResponseSchema, UpdateSchema, to_response_schema, to_tax_response_schema
from . import repository
from .donation import donation_router
from .services import calculate_taxes

router = APIRouter(prefix="/api/subsidy")
router.include_router(donation_router)


@router.get("", response_model=list[ResponseSchema])
def get_all(session: Session = Depends(get_session)):
    return [
        to_response_schema(record)
        for record in repository.get_all(session)
    ]

@router.get("/tax")
def get_taxes(session: Session = Depends(get_session)):
    return to_tax_response_schema(calculate_taxes(session))

@router.get("/{key}", response_model=UpdateSchema)
def get(key: int, session: Session = Depends(get_session)):
    return repository.get(session, key)

@router.post("", response_model=ResponseSchema)
def create(data: CreateSchema, session: Session = Depends(get_session)):
    return repository.create(session, data)

@router.put("/{key}", response_model=ResponseSchema)
def update(key: int, data: UpdateSchema, session: Session = Depends(get_session)):
    return repository.update(session, key, data)

@router.delete("/{key}", status_code=status.HTTP_204_NO_CONTENT)
def delete(key: int, session: Session = Depends(get_session)):
    repository.delete(session, key)
