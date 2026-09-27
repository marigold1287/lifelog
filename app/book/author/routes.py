from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db import get_session
from .schemas import CreateSchema, ResponseSchema, UpdateSchema, to_response_schema
from app.book.work.schemas import to_response_schema as to_work_response_schema, ResponseSchema as WorkResponseSchema
from . import repository

router = APIRouter(prefix="/api/author")


@router.get("", response_model=list[ResponseSchema])
def get_all(session: Session = Depends(get_session)):
    authors = repository.get_all(session)
    return [
        to_response_schema(author)
        for author in authors
    ]

@router.get("/{key}", response_model=ResponseSchema)
def get(key: int, session: Session = Depends(get_session)):
    return to_response_schema(repository.get(session, key))

@router.get("/{key}/works", response_model=list[WorkResponseSchema])
def get_works(key: int, session: Session = Depends(get_session)):
    return [
        to_work_response_schema(work)
        for work in repository.get_works(session, key)
    ]

@router.post("", response_model=ResponseSchema)
def create(data: CreateSchema, session: Session = Depends(get_session)):
    return to_response_schema(repository.create(session, data))

@router.put("/{key}", response_model=ResponseSchema)
def update(key: int, data: UpdateSchema, session: Session = Depends(get_session)):
    return to_response_schema(repository.update(session, key, data))

@router.delete("/{key}", status_code=status.HTTP_204_NO_CONTENT)
def delete(key: int, session: Session = Depends(get_session)):
    repository.delete(session, key)
