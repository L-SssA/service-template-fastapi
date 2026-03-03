"""
示例 Celery 任务
"""
import time
from loguru import logger
from celery_tasks import celery_app


@celery_app.task(name="celery_tasks.tasks.example.add_task")
def add_task(a: int, b: int) -> int:
    """
    简单的加法任务

    Args:
        a: 第一个数
        b: 第二个数

    Returns:
        两数之和
    """
    logger.info(f"执行加法任务：{a} + {b}")
    result = a + b
    logger.success(f"加法任务完成，结果：{result}")
    return result


@celery_app.task(name="celery_tasks.tasks.example.sleep_task")
def sleep_task(seconds: int) -> str:
    """
    延迟响应测试任务

    Args:
        seconds: 睡眠秒数

    Returns:
        完成消息
    """
    logger.info(f"开始睡眠 {seconds} 秒")
    time.sleep(seconds)
    logger.success(f"睡眠任务完成，共睡眠 {seconds} 秒")
    return f"Sleep completed for {seconds} seconds"
