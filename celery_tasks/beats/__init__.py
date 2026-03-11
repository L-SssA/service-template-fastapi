"""
Celery Beat 定时任务定义

在此目录下管理所有定时任务
"""
from .example import print_time_task, cleanup_task, health_check_task
from .business import (
    notify_overdue_orders,
    clear_expired_sessions,
    sync_data_task,
    calculate_statistics,
    send_daily_report,
    backup_database
)


__all__ = [
    'print_time_task',
    'cleanup_task',
    'health_check_task',
    'notify_overdue_orders',
    'clear_expired_sessions',
    'sync_data_task',
    'calculate_statistics',
    'send_daily_report',
    'backup_database'
]
