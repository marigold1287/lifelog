from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db import get_session
from .schemas import ResponseSchema, InputSchema, InputResponseSchema, to_response_schema, to_input_schema
from . import repository

router = APIRouter(prefix="/api/work")

@router.get("", response_model=list[ResponseSchema])
def get_all(session: Session = Depends(get_session)):
    works = repository.get_all(session)

    return [
        to_response_schema(work)
        for work in works
    ]

@router.get("/{key}", response_model=InputResponseSchema)
def get(key: int, session: Session = Depends(get_session)):
    return to_input_schema(repository.get(session, key))

@router.post("", response_model=ResponseSchema)
def create(data: InputSchema, session: Session = Depends(get_session)):
    return to_response_schema(repository.create(session, data))

@router.put("/{key}", response_model=ResponseSchema)
def update(key: int, data: InputSchema, session: Session = Depends(get_session)):
    return to_response_schema(repository.update(session, key, data))

@router.delete("/{key}", status_code=status.HTTP_204_NO_CONTENT)
def delete(key: int, session: Session = Depends(get_session)):
    repository.delete(session, key)