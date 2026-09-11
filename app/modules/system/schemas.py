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
    connected: bool = Field(..., description="是否连接成功")
    workers: int = Field(0, description="worker 数量")
    error: Optional[str] = Field(None, description="错误信息")


class CeleryStatusResponse(BaseResponse):
    """Celery 状态响应"""
    data: Optional[CeleryStatusData] = Field(..., description="Celery 状态数据")
