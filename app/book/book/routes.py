from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_session
from .schemas import ResponseSchema, to_response_schema
from . import repository

router = APIRouter(prefix="/api/book")

# ブックリストというよりは読書記録リストが返される。
@router.get("", response_model=list[ResponseSchema])
def get_all(session: Session = Depends(get_session)):
    books = repository.get_all(session)

    return [
        record
        for book in books
        for record in to_response_schema(book)
    ]