"""
异步任务通用管理路由
提供对所有异步任务的统一管理接口，包括状态查询、任务取消等
"""
from loguru import logger

from app.utils.decorators import exception_handler
from app.routers.base import create_router
from app.models.task import (
    TaskInfo,
    TaskInfoResponse,
    CancelTaskRequest,
    CancelTaskResponse,
)
from app.utils.celery_client import get_task_result, get_task_status, revoke_task


router = create_router("tasks")


@router.get("/{task_id}", summary="获取任务信息和结果", response_model=TaskInfoResponse)
@exception_handler("获取任务信息")
async def get_task_info(task_id: str):
    """
    获取任务信息和结果

    适用于查询任何异步任务的执行状态和结果

    Args:
        task_id: 任务 ID

    Returns:
        任务状态和结果（如果已完成）

    Examples:
        - 查询任务状态：GET /tasks/{task_id}
        - 成功任务会返回 result 字段
        - 失败任务会返回 error 字段
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


@router.delete("/{task_id}", summary="取消/终止任务", response_model=CancelTaskResponse)
@exception_handler("取消任务")
async def cancel_task(task_id: str, request: CancelTaskRequest):
    """
    取消/终止任务

    可以取消正在执行的任务或终止已启动的任务

    Args:
        task_id: 任务 ID
        request: 包含是否强制终止的参数
            - terminate: True 表示强制终止正在运行的任务，False 仅取消未开始的任务

    Returns:
        操作结果

    Examples:
        - 仅取消未开始的任务：DELETE /tasks/{task_id} {"terminate": false}
        - 强制终止运行中的任务：DELETE /tasks/{task_id} {"terminate": true}

    Note:
        - terminate=False: 只取消尚未开始执行的任务
        - terminate=True: 会强制终止正在执行的任务（可能导致数据不一致）
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
