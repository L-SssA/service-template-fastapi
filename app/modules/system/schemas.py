"""
系统管理相关的模型定义
用于系统健康检查、服务状态监控等管理接口
"""
from typing import Optional
from pydantic import Field

from app.shared.schemas import IBaseModel, BaseResponse


# ============== Response Models ==============
class CeleryStatusData(IBaseModel):
    """Celery 状态数据"""
    status: str = Field(..., description="Celery 状态")
    message: str = Field(..., description="状态消息")
    test_task_result: Optional[str] = Field(None, description="测试任务结果")


class CeleryStatusResponse(BaseResponse):
    """Celery 状态响应"""
    data: CeleryStatusData = Field(..., description="Celery 状态数据")
