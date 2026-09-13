from celery import Celery
from . import config
from .tasks import load_tasks

# 加载任务
load_tasks()
# 创建 Celery 实例
app = Celery(
    'celery_app',
    broker=config.broker_url,
    backend=config.result_backend,
)

# 应用配置
app.conf.update(
    task_serializer=config.task_serializer,
    result_serializer=config.result_serializer,
    accept_content=config.accept_content,
    timezone=config.timezone,
    enable_utc=config.enable_utc,
    worker_hijack_root_logger=False,
    worker_log_level=config.log_level,

    # Windows 兼容性设置
    event_loop='asyncio',

    # 任务路由配置
    task_routes={},

    # 结果过期时间（秒）
    result_expires=3600,

    # 任务重试配置
    task_default_retry_delay=60,
    task_max_retry_delay=3600,

    # Beat 定时任务配置
    beat_schedule={
        # 每分钟打印时间
        # "print-time-every-minute": {
        #     "task": "celery_app.beats.example.print_time_task",
        #     "schedule": 5.0,
        # },
    },
    beat_scheduler_timezone=config.timezone,
)
