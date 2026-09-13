"""
Celery 客户端工具类
用于 FastAPI 应用中调用 Celery 异步任务
"""
from typing import Any, List, Dict, Optional
from celery.result import AsyncResult
from loguru import logger


class CeleryClient:
    """Celery 客户端封装类"""
    _celery_instance = None

    @property
    def app(self):
        """获取 Celery 应用实例（懒加载）"""

        if not self._celery_instance:
            from celery_app.server import app
            self._celery_instance = app

        return self._celery_instance

    def send_task(
        self,
        task_name: str,
        args: Optional[List[Any]] = [],
        kwargs: Optional[Dict[str, Any]] = {},
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
        return self.app.send_task(
            task_name,
            args=args,
            kwargs=kwargs,
            **options
        )

    def get_task_result(
        self,
        task_id: str,
        timeout: Optional[int] = None
    ) -> Any:
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
        return AsyncResult(task_id, app=self.app).get(timeout=timeout)

    def get_task_status(
        self,
        task_id: str
    ) -> str:
        """
        获取任务状态

        Args:
            task_id: 任务 ID

        Returns:
            任务状态字符串 (PENDING, STARTED, RETRY, SUCCESS, FAILURE)
        """
        return AsyncResult(task_id, app=self.app).state

    def revoke_task(
        self,
        task_id: str,
        terminate: bool = False,
        signal: str = 'SIGTERM'
    ) -> None:
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
        self.app.control.revoke(task_id, terminate=terminate, signal=signal)

    def check_celery_connection(
        self,
        timeout: int = 3
    ) -> dict:
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

        result = {
            "connected": False,
            "workers_count": 0,
            "workers": {},
            "error": "",
        }

        try:
            # 检查 Redis 连接
            conn = self.app.connection()
            conn.ensure_connection(max_retries=3)

            # 检查 Worker 状态
            insp = self.app.control.inspect(timeout=timeout)
            workers = insp.active()

            result["connected"] = True
            result["workers_count"] = len(workers) if workers else 0
            result["workers"] = workers or {}
            result["error"] = None if workers else "未检测到活跃的 Celery Worker"

            return result
        except Exception as e:
            result["error"] = str(e)
            return result

    def is_celery_available(
        self,
        timeout: int = 3
    ) -> bool:
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
        result = self.check_celery_connection(timeout)
        return result["connected"] and result["workers_count"] > 0

    def check_celery_status(
        self,
    ):
        """
        检查 Celery 连接状态并输出日志

        Returns:
            dict: 检查结果
        """

        result = self.check_celery_connection(timeout=3)

        if result["connected"]:
            if result["workers_count"] > 0:
                logger.success(
                    f"检测到 {result['workers_count']} 个活跃的 Celery Worker")
            else:
                logger.warning("未检测到活跃的 Celery Worker，异步任务可能无法执行")
                logger.warning(f"提示：{result['error']}")
        else:
            logger.warning(f"Celery 连接失败：{result['error']}")
            logger.warning("异步任务功能将不可用，请确保 Redis 和 Celery Worker 已启动")

        return result


celery_client = CeleryClient()
