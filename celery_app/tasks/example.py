from loguru import logger
from celery import shared_task

@shared_task(name="celery_app.tasks.example.add_task")
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
