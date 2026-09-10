from fastapi import APIRouter
from .publisher import publisher_router
from .work import work_router
from .author import author_router
from .book import book_router


router = APIRouter()

router.include_router(publisher_router)
router.include_router(work_router)
router.include_router(author_router)
router.include_router(book_router)