"""
系统管理相关的路由
提供系统健康检查、服务状态监控等管理接口
"""
from loguru import logger

from app.utils.decorators import exception_handler
from app.routers.base import create_router
from app.models.system import (
    CeleryStatusData,
    CeleryStatusResponse,
)
from app.utils.celery_client import send_task


router = create_router("system")


@router.get("/celery-status", summary="检查 Celery 服务状态", response_model=CeleryStatusResponse)
@exception_handler("检查 Celery 状态")
async def celery_status():
    """
    检查 Celery 服务状态

    用于验证 Celery Worker 是否正常运行，通过发送一个测试任务来检测

    Returns:
        Celery 服务状态信息

    Example:
        >>> GET /system/celery-status
        {
            "code": 200,
            "data": {
                "status": "healthy",
                "message": "Celery Worker is available",
                "test_task_result": "2"
            },
            "message": "Celery Worker is available"
        }
    """
    # 发送一个简单的测试任务
    result = send_task(
        "celery_tasks.tasks.example.add_task",
        args=[1, 1]
    )
    task_result = result.get(timeout=5)

    return CeleryStatusResponse(
        code=200,
        data=CeleryStatusData(
            status="healthy",
            message="Celery Worker is available",
            test_task_result=str(task_result),
        ),
        message="Celery Worker is available"
    )
