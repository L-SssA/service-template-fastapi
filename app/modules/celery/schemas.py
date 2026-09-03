"""
Celery 异步任务相关的模型定义
注意：通用的任务管理模型（TaskInfo, CancelTaskRequest 等）已移至 app/models/task.py
"""
from typing import Optional
from pydantic import Field

from app.shared.schemas import IBaseModel, BaseResponse


# ============== Request Models ==============
class AddTaskRequest(IBaseModel):
    """加法任务请求模型"""
    a: int = Field(..., description="第一个数")
    b: int = Field(..., description="第二个数")


class SleepTaskRequest(IBaseModel):
    """睡眠任务请求模型"""
    seconds: int = Field(..., description="睡眠秒数")
    delay: Optional[int] = Field(0, description="延迟执行时间（秒）")  # 延迟执行时间（秒）


class LogTaskRequest(IBaseModel):
    """日志任务请求模型"""
    level: str = Field("info", description="日志级别")
    message: str = Field("Test log message", description="日志内容")


class CustomTaskRequest(IBaseModel):
    """自定义任务请求模型"""
    task_name: str = Field(..., description="任务名称")
    args: list = Field(default_factory=list, description="位置参数")
    kwargs: dict = Field(default_factory=dict, description="关键字参数")


# ============== Response Models ==============
class TaskData(IBaseModel):
    """任务数据"""
    task_id: str = Field(..., description="任务ID")
    status: str = Field(..., description="任务状态")
    delay: Optional[int] = Field(None, description="延迟执行时间（秒）")


class TaskResponse(BaseResponse):
    """任务响应"""
    data: TaskData = Field(..., description="任务数据")
