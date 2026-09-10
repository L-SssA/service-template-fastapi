import traceback

from typing import Any
from loguru import logger


class HttpException(Exception):
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

class InvalidTokenException(HttpException):
    def __init__(self):
        super().__init__(status_code=403, message="Token不存在或已过期，请重新登陆。")

class AccessTokenRequiredException(HttpException):
    def __init__(self):
        super().__init__(status_code=403, message="请使用Access_Token访问")

class RefreshTokenRequiredException(HttpException):
    def __init__(self):
        super().__init__(status_code=403, message="请使用Refresh_Token访问")

class PermissionNotAllowedException(HttpException):
    def __init__(self):
        super().__init__(status_code=403, message="您没有权限执行此操作")
