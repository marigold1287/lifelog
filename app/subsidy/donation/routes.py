from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db import get_session
from .schemas import CreateSchema, ResponseSchema, UpdateSchema, EntryListSchema, to_entry_list_schema, to_response_schema, CreateUpdateResponse
from . import repository

router = APIRouter(prefix="/donation")


@router.get("", response_model=list[ResponseSchema])
def get_all(session: Session = Depends(get_session)):
    return [
        to_response_schema(record)
        for record in repository.get_all(session)
    ]

@router.get("/entry", response_model=list[EntryListSchema])
def get_entries_without_donation_deduction(
    entry_id: int | None = None,
    session: Session = Depends(get_session),
):
    entries = repository.get_entries_without_donation_deduction(
        session,
        entry_id=entry_id,
    )
    return [to_entry_list_schema(entry) for entry in entries]


@router.get("/{key}", response_model=UpdateSchema)
def get(key: int, session: Session = Depends(get_session)):
    return repository.get(session, key)

@router.post("", response_model=CreateUpdateResponse)
def create(data: CreateSchema, session: Session = Depends(get_session)):
    return repository.create(session, data)

@router.put("/{key}", response_model=CreateUpdateResponse)
def update(key: int, data: UpdateSchema, session: Session = Depends(get_session)):
    return repository.update(session, key, data)

@router.delete("/{key}", status_code=status.HTTP_204_NO_CONTENT)
def delete(key: int, session: Session = Depends(get_session)):
    repository.delete(session, key)
