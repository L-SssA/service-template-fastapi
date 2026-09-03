import traceback
from typing import Any

from loguru import logger


class HttpException(Exception):
    def __init__(self, status_code: int, message: str = '接口处理异常', data: Any = None):
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
