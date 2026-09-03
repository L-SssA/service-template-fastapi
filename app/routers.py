from fastapi import APIRouter
from .modules.books_example.routes import router as book_router
from .modules.celery.routes import router as celery_router
from .modules.system.routes import router as system_router
from .modules.tasks.routes import router as tasks_router
from .modules.auth.routes import router as auth_router


root_router = APIRouter()
root_router.include_router(book_router)
root_router.include_router(celery_router)
root_router.include_router(system_router)
root_router.include_router(tasks_router)
root_router.include_router(auth_router)
