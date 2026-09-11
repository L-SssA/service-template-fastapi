"""
异步任务通用模型定义
"""
from typing import Optional
from pydantic import Field

from app.shared.schemas import IBaseModel, BaseResponse


# ============== Common Response Models ==============
class TaskInfo(IBaseModel):
    """任务信息"""
    task_id: str = Field(..., description="任务ID")
    status: str = Field(..., description="任务状态")
    result: Optional[str] = Field(None, description="任务结果")
    error: Optional[str] = Field(None, description="错误信息")


class TaskInfoResponse(BaseResponse):
    """任务信息响应"""
    data: TaskInfo


class CancelTaskResponse(BaseResponse):
    """取消任务响应"""
    data: Optional[str]
