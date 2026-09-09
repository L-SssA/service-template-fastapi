from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.shared.exception_schemas import HttpException
from app.utils import http_utils


def validation_exception_handler(request: Request, e: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content=http_utils.get_response(
            code=400, data=e.errors(), message='参数错误'),
    )


def http_exception_handler(request: Request, e: HttpException):
    status_code = e.status_code if hasattr(e, "status_code") else 500
    data = e.data if hasattr(e, "data") else None
    message = e.message if hasattr(e, "message") else "操作失败"
    return JSONResponse(
        status_code=status_code,
        content=http_utils.get_response(status_code, data, message),
    )
