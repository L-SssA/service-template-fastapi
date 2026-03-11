from celery.schedules import crontab
import os
from app.utils import tools


# 加载配置文件
env = os.getenv("ENV", "dev")
env_config_file = os.path.join(os.path.dirname(
    os.path.dirname(__file__)), f"config.{env}.toml")
_env_config = tools.load_toml(env_config_file)


# Redis 配置
_redis_cfg: dict = _env_config.get("redis", {})
redis_host = _redis_cfg.get("host", "localhost")
redis_port = _redis_cfg.get("port", 6379)
redis_db = _redis_cfg.get("db", 0)
redis_password = _redis_cfg.get("password", "") or None


# Celery 配置
_celery_cfg: dict = _env_config.get("celery", {})
broker_url = _celery_cfg.get(
    "broker_url", f"redis://{redis_host}:{redis_port}/{redis_db}")
result_backend = _celery_cfg.get(
    "result_backend", f"redis://{redis_host}:{redis_port}/1")
task_serializer = _celery_cfg.get("task_serializer", "json")
result_serializer = _celery_cfg.get("result_serializer", "json")
accept_content = _celery_cfg.get("accept_content", ["json"])
timezone = _celery_cfg.get("timezone", "Asia/Shanghai")
enable_utc = _celery_cfg.get("enable_utc", True)


# Celery 配置字典
celery_config = {
    "broker_url": broker_url,
    "result_backend": result_backend,
    "task_serializer": task_serializer,
    "result_serializer": result_serializer,
    "accept_content": accept_content,
    "timezone": timezone,
    "enable_utc": enable_utc,
    "worker_hijack_root_logger": False,  # 不使用 Celery 的根日志，使用 Loguru
    "worker_log_level": _env_config.get("service", {}).get("log_level", "debug"),
}


# Celery Beat 定时任务配置
beat_schedule = {
    # ========== 示例任务 ==========
    # 每分钟打印时间
    "print-time-every-minute": {
        "task": "celery_tasks.beats.example.print_time_task",
        "schedule": 60.0,  # 每 60 秒执行一次
    },

    # 每小时执行清理任务
    "cleanup-every-hour": {
        "task": "celery_tasks.beats.example.cleanup_task",
        "schedule": crontab(minute=0, hour="*"),  # 每小时整点执行
    },

    # 每天早上 9 点执行健康检查
    "health-check-every-day": {
        "task": "celery_tasks.beats.example.health_check_task",
        "schedule": crontab(hour=9, minute=0),  # 每天 9:00 执行
    },

    # ========== 业务任务 ==========
    # 每天早上 10 点发送逾期订单提醒
    "notify-overdue-orders-daily": {
        "task": "celery_tasks.beats.business.notify_overdue_orders",
        "schedule": crontab(hour=10, minute=0),  # 每天 10:00 执行
    },

    # 每 30 分钟清理过期会话
    "clear-sessions-every-30min": {
        "task": "celery_tasks.beats.business.clear_expired_sessions",
        "schedule": 1800.0,  # 1800 秒 = 30 分钟
    },

    # 每小时同步外部数据
    "sync-data-every-hour": {
        "task": "celery_tasks.beats.business.sync_data_task",
        "schedule": crontab(minute=0, hour="*"),  # 每小时整点执行
    },

    # 每 15 分钟计算统计数据
    "calculate-stats-every-15min": {
        "task": "celery_tasks.beats.business.calculate_statistics",
        "schedule": 900.0,  # 900 秒 = 15 分钟
    },

    # 每天下午 6 点发送日报
    "send-daily-report-evening": {
        "task": "celery_tasks.beats.business.send_daily_report",
        "schedule": crontab(hour=18, minute=0),  # 每天 18:00 执行
    },

    # 每天凌晨 2 点备份数据库
    "backup-database-nightly": {
        "task": "celery_tasks.beats.business.backup_database",
        "schedule": crontab(hour=2, minute=0),  # 每天 02:00 执行
    },
}

# 时区设置（用于 Beat）
beat_scheduler_timezone = timezone
