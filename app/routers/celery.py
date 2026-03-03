"""
Celery 异步任务路由
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
    CustomTaskRequest,
    CancelTaskRequest,
    TaskInfo,
    CeleryStatusData,
    TaskData,
    CeleryStatusResponse,
    TaskResponse,
    TaskInfoResponse,
    CancelTaskResponse,
)
from app.utils.celery_client import send_task, get_task_result, get_task_status, revoke_task


router = create_router("celery")


# ============== API Endpoints ==============

@router.get("/status", summary="检查 Celery 服务状态", response_model=CeleryStatusResponse)
@exception_handler("检查 Celery 状态")
async def celery_status():
    """
    检查 Celery 服务状态

    Returns:
        Celery 服务状态信息
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


@router.get("/tasks/{task_id}", summary="获取任务信息和结果", response_model=TaskInfoResponse)
@exception_handler("获取任务信息")
async def get_task_info(task_id: str):
    """
    获取任务信息和结果

    Args:
        task_id: 任务 ID

    Returns:
        任务状态和结果（如果已完成）
    """
    status = get_task_status(task_id)

    task_info = TaskInfo(
        task_id=task_id,
        status=status,
    )

    # 如果任务已完成，尝试获取结果
    if status == "SUCCESS":
        try:
            result = get_task_result(task_id, timeout=2)
            task_info.result = str(result)
        except Exception as e:
            task_info.result_error = str(e)
    elif status == "FAILURE":
        try:
            result = get_task_result(task_id, timeout=2)
            task_info.error = str(result)
        except Exception as e:
            task_info.error = str(e)

    return TaskInfoResponse(
        code=200,
        data=task_info,
        message=f"Task status: {status}"
    )


@router.delete("/tasks/{task_id}", summary="取消/终止任务", response_model=CancelTaskResponse)
@exception_handler("取消任务")
async def cancel_task(task_id: str, request: CancelTaskRequest):
    """
    取消/终止任务

    Args:
        task_id: 任务 ID
        request: 包含是否强制终止的参数

    Returns:
        操作结果
    """
    revoke_task(task_id, terminate=request.terminate)
    action = "terminated" if request.terminate else "revoked"

    return CancelTaskResponse(
        code=200,
        data={
            "task_id": task_id,
            "message": f"Task has been {action}",
        },
        message=f"Task has been {action}"
    )
