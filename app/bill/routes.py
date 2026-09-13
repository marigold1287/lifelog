from fastapi import APIRouter, Depends, status
from .electric import electric_router


router = APIRouter()

router.include_router(electric_router)