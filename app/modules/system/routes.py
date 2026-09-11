"""
系统管理相关的路由
提供系统健康检查、服务状态监控等管理接口
"""
from app.utils.decorators import exception_handler
from app.shared.routes import create_router
from app.utils.celery_client import client
from app.utils import http_utils

from .schemas import (
    CeleryStatusData,
    CeleryStatusResponse,
)

router = create_router("system")


@router.get("/celery-status", summary="检查 Celery 服务状态", response_model=CeleryStatusResponse)
@exception_handler("检查 Celery 状态")
async def celery_status():
    """
    检查 Celery 服务状态

    用于验证 Celery Worker 是否正常运行

    Returns:
        Celery 服务状态信息
    """

    status = client.check_celery_connection()

    return http_utils.get_response(
        code=200,
        data={
            "connected": status["connected"],
            "workers_count": status["workers_count"],
            "error": status["error"],
        },
        message="操作成功"
    )
