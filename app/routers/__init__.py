from fastapi import APIRouter
from .example import router as example_router
from .celery import router as celery_router


root_router = APIRouter()
root_router.include_router(example_router)
root_router.include_router(celery_router)
