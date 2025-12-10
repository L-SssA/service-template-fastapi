from fastapi import APIRouter
from .example import router as example_router


root_router = APIRouter()
root_router.include_router(example_router)
