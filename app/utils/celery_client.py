"""
Celery 客户端工具类
用于 FastAPI 应用中调用 Celery 异步任务
"""
from typing import Any, List, Dict, Optional
from celery.result import AsyncResult


def send_task(
    task_name: str,
    args: Optional[List[Any]] = None,
    kwargs: Optional[Dict[str, Any]] = None,
    **options
) -> AsyncResult:
    """
    发送异步任务到 Celery Worker

    Args:
        task_name: 任务名称（如："celery_tasks.tasks.example.add_task"）
        args: 任务参数列表
        kwargs: 任务关键字参数
        **options: 其他 Celery 选项 (如：queue, priority, countdown 等)

    Returns:
        AsyncResult 对象，用于追踪任务状态和获取结果

    Examples:
        >>> result = send_task("celery_tasks.tasks.example.add_task", args=[1, 2])
        >>> print(result.get(timeout=10))
        3

        >>> result = send_task(
        ...     "celery_tasks.tasks.example.sleep_task",
        ...     args=[5],
        ...     countdown=10  # 延迟 10 秒执行
        ... )
    """
    from celery_tasks import celery_app

    if args is None:
        args = []
    if kwargs is None:
        kwargs = {}

    # 使用 send_task 方法，不直接导入任务函数
    result = celery_app.send_task(
        task_name,
        args=args,
        kwargs=kwargs,
        **options
    )

    return result


def get_task_result(task_id: str, timeout: Optional[int] = None) -> Any:
    """
    获取已完成任务的结果

    Args:
        task_id: 任务 ID
        timeout: 等待超时时间（秒），None 表示无限等待

    Returns:
        任务执行结果

    Raises:
        Exception: 任务执行失败时抛出异常
    """
    from celery_tasks import celery_app

    result = AsyncResult(task_id, app=celery_app)
    return result.get(timeout=timeout)


def get_task_status(task_id: str) -> str:
    """
    获取任务状态

    Args:
        task_id: 任务 ID

    Returns:
        任务状态字符串 (PENDING, STARTED, RETRY, SUCCESS, FAILURE)
    """
    from celery_tasks import celery_app

    result = AsyncResult(task_id, app=celery_app)
    return result.state


def revoke_task(task_id: str, terminate: bool = False, signal: str = 'SIGTERM') -> None:
    """
    撤销/终止任务

    Args:
        task_id: 任务 ID
        terminate: 是否强制终止正在运行的任务
        signal: 终止信号类型

    Examples:
        >>> revoke_task("task-id-here")  # 撤销未开始的任务
        >>> revoke_task("task-id-here", terminate=True)  # 终止正在运行的任务
    """
    from celery_tasks import celery_app

    celery_app.control.revoke(task_id, terminate=terminate, signal=signal)


def check_celery_connection(timeout: int = 3) -> dict:
    """
    检查 Celery 连接性和 Worker 状态

    Args:
        timeout: 检查超时时间（秒）

    Returns:
        包含连接状态和 Worker 信息的字典
        - connected: bool - 是否已连接
        - workers_count: int - Worker 数量
        - workers: dict - Worker 详细信息
        - error: str - 错误信息（如果有）

    Examples:
        >>> result = check_celery_connection()
        >>> if result["connected"]:
        ...     print(f"检测到 {result['workers_count']} 个 Worker")
    """
    from celery_tasks import celery_app

    try:
        # 检查 Redis 连接
        conn = celery_app.connection()
        conn.ensure_connection(max_retries=3)

        # 检查 Worker 状态
        insp = celery_app.control.inspect(timeout=timeout)
        workers = insp.active()

        if workers:
            return {
                "connected": True,
                "workers_count": len(workers),
                "workers": workers,
                "error": None,
            }
        else:
            return {
                "connected": True,  # Redis 连接正常
                "workers_count": 0,
                "workers": {},
                "error": "未检测到活跃的 Celery Worker",
            }

    except Exception as e:
        return {
            "connected": False,
            "workers_count": 0,
            "workers": {},
            "error": str(e),
        }


def is_celery_available(timeout: int = 3) -> bool:
    """
    快速检查 Celery 是否可用

    Args:
        timeout: 检查超时时间（秒）

    Returns:
        True 如果 Celery 可用且有活跃 Worker，否则 False

    Examples:
        >>> if is_celery_available():
        ...     send_task("my_task", args=[1, 2])
        ... else:
        ...     logger.warning("Celery 不可用")
    """
    result = check_celery_connection(timeout)
    return result["connected"] and result["workers_count"] > 0
