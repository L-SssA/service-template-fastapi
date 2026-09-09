import traceback

from typing import Any
from loguru import logger
from fastapi import HTTPException


class HttpException(HTTPException):
    def __init__(self, status_code: int, message: str = '接口处理异常', data: Any = None):
        super().__init__(status_code=status_code, detail=message)
        self.message = message
        self.status_code = status_code
        self.data = data
        # 获取异常堆栈信息
        tb_str = traceback.format_exc().strip()
        if not tb_str or tb_str == "NoneType: None":
            msg = f'HttpException: {status_code}, {message}'
        else:
            msg = f'HttpException: {status_code}, {message}\n{tb_str}'

        logger.error(msg)
