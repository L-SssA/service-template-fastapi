# Celery Beat 定时任务快速开始

## 📚 概述

本项目已集成 Celery Beat 定时任务调度器，支持周期性执行任务。

## 🗂️ 目录结构

```
celery_tasks/
├── beats/                 # 定时任务定义
│   ├── __init__.py
│   ├── example.py         # 示例定时任务
│   └── business.py        # 业务定时任务
├── config.py              # 包含 beat_schedule 配置
└── beat.py                # Beat 启动入口
```

## 🚀 快速启动

### 方式 1: Worker + Beat 一体化（推荐）

**Windows:**

```bash
.\scripts\start_celery_worker_beat.bat
```

**Linux/macOS:**

```bash
celery -A celery_tasks worker --beat --loglevel=info
```

### 方式 2: 分别启动

**终端 1 - Worker:**

```bash
celery -A celery_tasks.worker worker --loglevel=info --pool=solo
```

**终端 2 - Beat:**

```bash
celery -A celery_tasks.beat beat --loglevel=info
```

## ✅ 内置定时任务

| 任务                   | 频率       | 说明         |
| ---------------------- | ---------- | ------------ |
| print_time_task        | 每 60 秒   | 打印当前时间 |
| cleanup_task           | 每小时     | 清理任务示例 |
| health_check_task      | 每天 9:00  | 健康检查     |
| notify_overdue_orders  | 每天 10:00 | 逾期订单提醒 |
| clear_expired_sessions | 每 30 分钟 | 清理过期会话 |
| sync_data_task         | 每小时     | 数据同步     |
| calculate_statistics   | 每 15 分钟 | 统计计算     |
| send_daily_report      | 每天 18:00 | 发送日报     |
| backup_database        | 每天 02:00 | 数据库备份   |

## 📝 添加新任务

### 1. 创建任务

在 `celery_tasks/beats/` 目录下创建：

```python
from celery_tasks.celery_app import app as celery_app

@celery_app.task(name="celery_tasks.beats.my_module.my_task")
def my_task():
    """我的定时任务"""
    print("执行任务")
    return "完成"
```

### 2. 配置调度计划

编辑 `celery_tasks/config.py`，在 `beat_schedule` 中添加：

```python
from celery.schedules import crontab

beat_schedule = {
    # ... 现有任务 ...

    # 新增任务
    "my-custom-task": {
        "task": "celery_tasks.beats.my_module.my_task",
        "schedule": 300.0,  # 每 300 秒（5 分钟）
    },
}
```

### 3. 重启服务

重新启动 Worker 和 Beat 使配置生效。

## 🔧 调度方式

### 固定间隔（秒数）

```python
"task-every-5-minutes": {
    "task": "myapp.tasks.my_task",
    "schedule": 300.0,
}
```

### Crontab 表达式

```python
from celery.schedules import crontab

# 每天早上 9 点
"every-morning-9am": {
    "task": "myapp.tasks.morning_task",
    "schedule": crontab(hour=9, minute=0),
}

# 每周一上午 10 点
"every-monday-10am": {
    "task": "myapp.tasks.weekly_task",
    "schedule": crontab(hour=10, minute=0, day_of_week=1),
}

# 每月 1 号凌晨
"first-of-month": {
    "task": "myapp.tasks.monthly_task",
    "schedule": crontab(hour=0, minute=0, day_of_month=1),
}
```

## 📖 详细文档

完整使用指南请参考：[CELERY_USAGE.md](CELERY_USAGE.md)

## ⚠️ 注意事项

1. **Beat 只负责调度**：Beat 本身不执行任务，只负责触发
2. **必须配合 Worker**：任务需要 Worker 来执行
3. **Windows 兼容性**：Worker 必须使用 `--pool=solo` 参数
4. **时区设置**：确保 `timezone` 和 `beat_scheduler_timezone` 一致

## 🐛 常见问题

### Q: Beat 启动了但任务没执行？

A: 确认 Worker 正在运行

### Q: 如何查看任务执行情况？

A: 查看 Worker 的日志输出

### Q: 如何禁用某个任务？

A: 注释掉 `beat_schedule` 中对应的配置

---

**版本**: v1.0.0  
**最后更新**: 2026-03-05
