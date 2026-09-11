"""
Celery 异步任务示例路由
提供具体的任务创建接口（如加法、睡眠、日志测试等）
"""
from app.shared.routes import create_router
from app.utils.decorators import exception_handler
from app.utils.celery_client import client

from .schemas import (
    TaskData,
    TaskResponse,
)

router = create_router("celery")

@router.post("/tasks/add", summary="创建加法异步任务", response_model=TaskResponse)
@exception_handler("创建加法任务")
async def create_add_task(a: int, b: int):
    """
    创建加法异步任务

    Args:
        request: 包含两个加数的请求体

    Returns:
        任务 ID 和状态
    """
    result = client.send_task(
        "celery_app.tasks.example.add_task",
        args=[a, b]
    )

    res_data = TaskData(task_id=result.id, status="pending")

    return TaskResponse(code=200, data=res_data, message=f"Add Task Created: {a} + {b}")
