"""
异步任务通用模型定义
"""
from typing import Optional
from app.models.base import IBaseModel, BaseResponse


# ============== Request Models ==============
class CancelTaskRequest(IBaseModel):
    """取消任务请求模型"""
    terminate: bool = False


# ============== Common Response Models ==============
class TaskInfo(IBaseModel):
    """任务信息"""
    task_id: str
    status: str
    result: Optional[str] = None
    result_error: Optional[str] = None
    error: Optional[str] = None


class TaskInfoResponse(BaseResponse):
    """任务信息响应"""
    data: TaskInfo


class CancelTaskResponse(BaseResponse):
    """取消任务响应"""
    data: dict
