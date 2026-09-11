"""
Celery 异步任务相关的模型定义
注意：通用的任务管理模型（TaskInfo, CancelTaskRequest 等）已移至 app/models/task.py
"""
from typing import Optional
from pydantic import Field

from app.shared.schemas import IBaseModel, BaseResponse


# ============== Response Models ==============
class TaskData(IBaseModel):
    """任务数据"""
    task_id: str = Field(..., description="任务ID")
    status: str = Field(..., description="任务状态")


class TaskResponse(BaseResponse):
    """任务响应"""
    data: Optional[TaskData] = Field(..., description="任务数据")
