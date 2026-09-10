from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_session
from .schemas import ResponseSchema
from . import repository

router = APIRouter(prefix="/api/book")


@router.get("", response_model=list[ResponseSchema])
def get_all(session: Session = Depends(get_session)):
    return repository.get_all(session)