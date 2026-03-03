"""
Celery 任务模块
所有异步任务都应该放在这个包中
"""

# 自动导入所有任务模块
from . import example
from . import logger_task

__all__ = ['example', 'logger_task']
