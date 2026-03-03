from celery import Celery
from .config import celery_config


# 创建 Celery 实例
celery_app = Celery(
    'celery_tasks',
    broker=celery_config['broker_url'],
    backend=celery_config['result_backend'],
)

# 应用配置
celery_app.conf.update(
    task_serializer=celery_config['task_serializer'],
    result_serializer=celery_config['result_serializer'],
    accept_content=celery_config['accept_content'],
    timezone=celery_config['timezone'],
    enable_utc=celery_config['enable_utc'],
    worker_hijack_root_logger=celery_config['worker_hijack_root_logger'],
    worker_log_level=celery_config['worker_log_level'],

    # Windows 兼容性设置
    event_loop='asyncio',

    # 任务路由配置
    task_routes={},

    # 结果过期时间（秒）
    result_expires=3600,

    # 任务重试配置
    task_default_retry_delay=60,
    task_max_retry_delay=3600,
)

# 自动发现任务
celery_app.autodiscover_tasks(['celery_tasks.tasks'])
