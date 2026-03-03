"""
Celery 异步任务示例路由
提供具体的任务创建接口（如加法、睡眠、日志测试等）
"""
from loguru import logger
import time

from app.utils import http_utils
from app.utils.decorators import exception_handler
from app.routers.base import create_router
from app.models.celery import (
    AddTaskRequest,
    SleepTaskRequest,
    LogTaskRequest,
    TaskData,
    TaskResponse,
)
from app.utils.celery_client import send_task


router = create_router("celery")


@router.post("/tasks/add", summary="创建加法异步任务", response_model=TaskResponse)
@exception_handler("创建加法任务")
async def create_add_task(request: AddTaskRequest):
    """
    创建加法异步任务

    Args:
        request: 包含两个加数的请求体

    Returns:
        任务 ID 和状态
    """
    result = send_task(
        "celery_tasks.tasks.example.add_task",
        args=[request.a, request.b]
    )

    return TaskResponse(
        code=200,
        data=TaskData(
            task_id=result.id,
            status="pending",
        ),
        message=f"Task created: {request.a} + {request.b}"
    )


@router.post("/tasks/sleep", summary="创建睡眠异步任务", response_model=TaskResponse)
@exception_handler("创建睡眠任务")
async def create_sleep_task(request: SleepTaskRequest):
    """
    创建睡眠异步任务

    Args:
        request: 包含睡眠秒数和可选延迟的请求体

    Returns:
        任务 ID 和状态
    """
    options = {}
    if request.delay > 0:
        options["countdown"] = request.delay

    result = send_task(
        "celery_tasks.tasks.example.sleep_task",
        args=[request.seconds],
        **options
    )

    return TaskResponse(
        code=200,
        data=TaskData(
            task_id=result.id,
            status="pending",
            delay=request.delay if request.delay > 0 else None,
        ),
        message=f"Sleep task created for {request.seconds} seconds"
    )


@router.post("/tasks/log", summary="创建日志测试异步任务", response_model=TaskResponse)
@exception_handler("创建日志任务")
async def create_log_task(request: LogTaskRequest):
    """
    创建日志测试异步任务

    Args:
        request: 包含日志级别和消息的请求体

    Returns:
        任务 ID 和状态
    """
    result = send_task(
        "celery_tasks.tasks.logger_task.log_message",
        args=[request.level, request.message]
    )

    return TaskResponse(
        code=200,
        data=TaskData(
            task_id=result.id,
            status="pending",
        ),
        message=f"Log task created: [{request.level.upper()}] {request.message}"
    )
