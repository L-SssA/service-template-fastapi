from loguru import logger
from celery import shared_task

@shared_task(name="celery_app.tasks.example.division_task")
def division_task(a: int, b: int) -> int:
    logger.info(f"执行除法任务：{a} / {b}")
    result = a / b
    logger.success(f"除法任务完成，结果：{result}")
    return result
