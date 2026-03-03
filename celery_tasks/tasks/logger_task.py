"""
日志测试 Celery 任务
用于验证异步任务中的日志输出格式与主应用一致
"""
from loguru import logger
from celery_tasks import celery_app


@celery_app.task(name="celery_tasks.tasks.logger_task.log_message")
def log_message(level: str = "info", message: str = "Test log message") -> str:
    """
    日志消息测试任务

    Args:
        level: 日志级别 (debug, info, success, warning, error)
        message: 日志消息内容

    Returns:
        执行结果消息
    """
    logger.info(f"收到日志任务：level={level}, message={message}")

    # 根据级别记录日志
    if level.lower() == "debug":
        logger.debug(message)
    elif level.lower() == "info":
        logger.info(message)
    elif level.lower() == "success":
        logger.success(message)
    elif level.lower() == "warning":
        logger.warning(message)
    elif level.lower() == "error":
        logger.error(message)
    else:
        logger.info(f"[{level.upper()}] {message}")

    result = f"日志已记录：[{level.upper()}] {message}"
    logger.success(result)
    return result


@celery_app.task(name="celery_tasks.tasks.logger_task.multi_level_logs")
def multi_level_logs(count: int = 5) -> str:
    """
    多级别日志测试任务

    Args:
        count: 每种级别日志的数量

    Returns:
        执行结果消息
    """
    logger.info(f"开始多级别日志测试，每种级别 {count} 条")

    for i in range(count):
        logger.debug(f"DEBUG 日志 #{i+1}")
        logger.info(f"INFO 日志 #{i+1}")
        logger.success(f"SUCCESS 日志 #{i+1}")
        logger.warning(f"WARNING 日志 #{i+1}")
        logger.error(f"ERROR 日志 #{i+1}")

    result = f"完成多级别日志测试，共生成 {count * 5} 条日志"
    logger.success(result)
    return result
