from datetime import datetime
from celery import shared_task
from loguru import logger

@shared_task(name="celery_app.beats.example.print_time_task")
def print_time_task():
    """
    打印当前时间的定时任务

    此任务用于演示 Celery Beat 的基本用法
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.success(f"[定时任务] 当前时间：{current_time}")
    return f"Current time: {current_time}"
