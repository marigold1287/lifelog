from fastapi import APIRouter
from .electric import electric_router
from .water import water_router
from .gas import gas_router



router = APIRouter()

router.include_router(electric_router)
router.include_router(water_router)
router.include_router(gas_router)