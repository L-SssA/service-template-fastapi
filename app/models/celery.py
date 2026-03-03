"""
Celery 异步任务相关的模型定义
注意：通用的任务管理模型（TaskInfo, CancelTaskRequest 等）已移至 app/models/task.py
"""
from typing import Optional
from app.models.base import IBaseModel, BaseResponse


# ============== Request Models ==============
class AddTaskRequest(IBaseModel):
    """加法任务请求模型"""
    a: int
    b: int


class SleepTaskRequest(IBaseModel):
    """睡眠任务请求模型"""
    seconds: int
    delay: Optional[int] = 0  # 延迟执行时间（秒）


class LogTaskRequest(IBaseModel):
    """日志任务请求模型"""
    level: str = "info"
    message: str = "Test log message"


class CustomTaskRequest(IBaseModel):
    """自定义任务请求模型"""
    task_name: str
    args: list = []
    kwargs: dict = {}


# ============== Response Models ==============
class CeleryStatusData(IBaseModel):
    """Celery 状态数据"""
    status: str
    message: str
    test_task_result: Optional[str] = None


class TaskData(IBaseModel):
    """任务数据"""
    task_id: str
    status: str
    delay: Optional[int] = None


class CeleryStatusResponse(BaseResponse):
    """Celery 状态响应"""
    data: CeleryStatusData


class TaskResponse(BaseResponse):
    """任务响应"""
    data: TaskData
