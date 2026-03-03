"""
系统管理相关的模型定义
用于系统健康检查、服务状态监控等管理接口
"""
from typing import Optional
from app.models.base import IBaseModel, BaseResponse


# ============== Response Models ==============
class CeleryStatusData(IBaseModel):
    """Celery 状态数据"""
    status: str
    message: str
    test_task_result: Optional[str] = None


class CeleryStatusResponse(BaseResponse):
    """Celery 状态响应"""
    data: CeleryStatusData
