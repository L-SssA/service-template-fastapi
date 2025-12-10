from fastapi import APIRouter


def create_router(sign):
    router = APIRouter()
    router.tags = [sign]
    router.prefix = f'/{sign}'
    return router
