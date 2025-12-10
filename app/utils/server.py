from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.models.exception import HttpException
from app.utils import http_utils


def validation_exception_handler(request: Request, e: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content=http_utils.get_response(
            code=400, data=e.errors(), message='参数错误'),
    )


def http_exception_handler(request: Request, e: HttpException):
    return JSONResponse(
        status_code=e.status_code,
        content=http_utils.get_response(
            code=e.status_code, data=e.data, message=e.message),
    )
