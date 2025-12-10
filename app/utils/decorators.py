import functools
from loguru import logger
import time
import warnings
from functools import wraps

from app.models.exception import HttpException


def exception_handler(operation_name: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except HttpException:
                raise
            except Exception:
                return HttpException(status_code=500, message=f"{operation_name}失败")
        return wrapper
    return decorator


def timer(description):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger.info(f"开始{description}")
            start_time = time.time()
            result = func(*args, **kwargs)
            logger.success(
                f"{description}完成，耗时{time.time() - start_time:.2f}秒")
            return result
        return wrapper
    return decorator


def no_warning(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            return func(*args, **kwargs)
    return wrapper
