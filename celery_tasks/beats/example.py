"""
示例定时任务

演示如何编写和配置 Celery Beat 定时任务
"""
from datetime import datetime
from loguru import logger
from celery_tasks.celery_app import app as celery_app


@celery_app.task(name="celery_tasks.beats.example.print_time_task")
def print_time_task():
    """
    打印当前时间的定时任务

    此任务用于演示 Celery Beat 的基本用法
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[定时任务] 当前时间：{current_time}")
    return f"Current time: {current_time}"


@celery_app.task(name="celery_tasks.beats.example.cleanup_task")
def cleanup_task():
    """
    清理任务示例

    模拟定期清理过期数据的任务
    """
    logger.info("[定时任务] 开始执行清理任务")

    # 模拟清理逻辑
    cleaned_count = 0
    # 这里应该放置实际的清理代码
    # 例如：删除过期的数据库记录、清理临时文件等

    logger.success(f"[定时任务] 清理任务完成，共清理 {cleaned_count} 条记录")
    return {"cleaned_count": cleaned_count, "status": "success"}


@celery_app.task(name="celery_tasks.beats.example.health_check_task")
def health_check_task():
    """
    健康检查定时任务

    定期检查系统健康状态
    """
    logger.info("[定时任务] 执行健康检查")

    # 模拟健康检查
    checks = {
        "database": "ok",
        "redis": "ok",
        "cache": "ok"
    }

    all_healthy = all(status == "ok" for status in checks.values())

    if all_healthy:
        logger.success("[定时任务] 系统健康检查通过")
    else:
        logger.warning("[定时任务] 系统健康检查发现异常")

    return {"healthy": all_healthy, "checks": checks}
