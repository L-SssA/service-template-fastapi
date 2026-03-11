# Celery Beat 定时任务使用指南

## 概述

Celery Beat 是 Celery 的定时任务调度器，用于周期性地执行任务。它类似于 Linux 的 cron 服务，但具有以下优势：

- ✅ 使用 Python 代码配置，更灵活
- ✅ 支持多种调度方式（固定间隔、crontab、自定义）
- ✅ 与 FastAPI 应用无缝集成
- ✅ 统一的日志系统

## 目录结构

定时任务定义在 `celery_tasks/beats/` 目录下：

```
celery_tasks/
├── beat.py                # Beat 调度器启动入口 ⭐
├── config.py              # Celery 配置（包含 beat_schedule）
└── beats/                 # 定时任务定义 ⭐
    ├── __init__.py        # 包初始化
    ├── example.py         # 示例定时任务
    └── business.py        # 业务定时任务
```

启动脚本：

```
scripts/
└── start_celery.py    # Celery 统一启动脚本（跨平台） ⭐
```

## 快速开始

### 方式 1: Worker + Beat 一体化启动（推荐，适合开发和测试）

**跨平台统一命令:**

```bash
# 使用 Python 脚本（推荐，跨平台）
uv run python scripts/start_celery.py all

# 或手动命令
# Windows
celery -A celery_tasks worker --beat --loglevel=info --pool=solo

# Linux/macOS
celery -A celery_tasks worker --beat --loglevel=info
```

### 方式 2: 分别启动 Worker 和 Beat（适合生产环境）

需要打开两个终端窗口：

**窗口 1 - 启动 Worker:**

```bash
# 跨平台统一命令（推荐）
uv run python scripts/start_celery.py worker

# 或手动命令
# Windows
celery -A celery_tasks.worker worker --loglevel=info --pool=solo

# Linux/macOS
celery -A celery_tasks.worker worker --loglevel=info
```

**窗口 2 - 启动 Beat 调度器:**

```bash
# 跨平台统一命令（推荐）
uv run python scripts/start_celery.py beat

# 或手动命令
celery -A celery_tasks.beat beat --loglevel=info
```

### 成功启动示例

Beat 启动成功的输出：

```
celery beat v5.3.0 (singularity)
Darwin-20.6.0-x86_64-i386-64bit 2026-03-05 10:00:00

[config]
.> app:      celery_tasks:0x...
.> broker:   redis://localhost:6379/0
.> loader:   celery.loaders.app.AppLoader
.> scheduler: celery.beat.PersistentScheduler

.> db:       /var/folders/.../celerybeat-schedule
.> log f:    [stderr]
.> logfile:  [2026-03-05 10:00:00,000: INFO/MainProcess] beat started.
```

Worker 执行定时任务的日志：

```
2026-03-05 10:01:00 | INFO | "./celery_tasks/beats/example.py:18": print_time_task - [定时任务] 当前时间：2026-03-05 10:01:00
2026-03-05 10:01:00 | SUCCESS | "./celery_tasks/beats/example.py:19": print_time_task - [定时任务] 时间打印完成
```

## 内置定时任务

项目已预配置以下定时任务：

### 示例任务

| 任务名称 | 功能说明           | 执行频率   | 任务路径                                       |
| -------- | ------------------ | ---------- | ---------------------------------------------- |
| 打印时间 | 每分钟打印当前时间 | 每 60 秒   | `celery_tasks.beats.example.print_time_task`   |
| 清理任务 | 模拟数据清理       | 每小时整点 | `celery_tasks.beats.example.cleanup_task`      |
| 健康检查 | 系统健康状态检查   | 每天 9:00  | `celery_tasks.beats.example.health_check_task` |

### 业务任务

| 任务名称     | 功能说明           | 执行频率   | 任务路径                                             |
| ------------ | ------------------ | ---------- | ---------------------------------------------------- |
| 逾期订单提醒 | 发送逾期订单通知   | 每天 10:00 | `celery_tasks.beats.business.notify_overdue_orders`  |
| 清理会话     | 清理过期用户会话   | 每 30 分钟 | `celery_tasks.beats.business.clear_expired_sessions` |
| 数据同步     | 同步外部数据       | 每小时整点 | `celery_tasks.beats.business.sync_data_task`         |
| 统计计算     | 计算实时统计数据   | 每 15 分钟 | `celery_tasks.beats.business.calculate_statistics`   |
| 发送日报     | 生成并发送每日报告 | 每天 18:00 | `celery_tasks.beats.business.send_daily_report`      |
| 数据库备份   | 执行数据库备份     | 每天 02:00 | `celery_tasks.beats.business.backup_database`        |

## 添加新的定时任务

### 步骤 1: 创建任务文件

在 `celery_tasks/beats/` 目录下创建新的任务文件：

```python
# celery_tasks/beats/my_task.py
from datetime import datetime
from loguru import logger
from celery_tasks.celery_app import app as celery_app


@celery_app.task(name="celery_tasks.beats.my_task.custom_task")
def custom_task():
    """
    自定义定时任务

    在此处编写你的业务逻辑
    """
    logger.info("[定时任务] 执行自定义任务")

    # 业务逻辑代码
    result = {"status": "success", "time": datetime.now().isoformat()}

    logger.success(f"[定时任务] 任务完成：{result}")
    return result
```

### 步骤 2: 配置调度计划

编辑 `celery_tasks/config.py`，在 `beat_schedule` 中添加新任务：

```python
from celery.schedules import crontab

beat_schedule = {
    # ... 现有任务 ...

    # 新增自定义任务
    "my-custom-task": {
        "task": "celery_tasks.beats.my_task.custom_task",
        "schedule": 300.0,  # 每 300 秒（5 分钟）执行一次
    },
}
```

### 步骤 3: 重启服务

重新启动 Worker 和 Beat 使配置生效。

## 调度方式

### 1. 固定间隔（秒数）

```python
beat_schedule = {
    "task-every-5-minutes": {
        "task": "myapp.tasks.my_task",
        "schedule": 300.0,  # 秒数
    },
}
```

### 2. Crontab 表达式

```python
from celery.schedules import crontab

beat_schedule = {
    # 每天早上 9 点
    "every-morning-9am": {
        "task": "myapp.tasks.morning_task",
        "schedule": crontab(hour=9, minute=0),
    },

    # 每周一上午 10 点
    "every-monday-10am": {
        "task": "myapp.tasks.weekly_task",
        "schedule": crontab(hour=10, minute=0, day_of_week=1),
    },

    # 每月 1 号凌晨 0 点
    "first-of-month": {
        "task": "myapp.tasks.monthly_task",
        "schedule": crontab(hour=0, minute=0, day_of_month=1),
    },
}
```

### 3. Crontab 高级用法

```python
# 工作日（周一至周五）早上 9 点
crontab(hour=9, minute=0, day_of_week='1-5')

# 每小时的前 10 分钟
crontab(minute='*/10')

# 每天的 9 点、12 点、18 点
crontab(hour='9,12,18', minute=0)

# 每 2 小时
crontab(minute=0, hour='*/2')
```

## 管理定时任务

### 查看已注册的任务

启动 Beat 后，会显示所有已注册的定时任务：

```
[2026-03-05 10:00:00,000: INFO/MainProcess] Writing entries...
[2026-03-05 10:00:00,000: INFO/MainProcess] tick: Added 10 new items to beat schedule
```

### 修改任务执行频率

直接编辑 `celery_tasks/config.py` 中的 `beat_schedule` 配置，然后重启服务。

### 临时禁用任务

注释掉 `beat_schedule` 中对应的任务配置即可：

```python
beat_schedule = {
    # "disabled-task": {  # 已禁用
    #     "task": "myapp.tasks.disabled",
    #     "schedule": 60.0,
    # },
}
```

### 动态调整（不推荐）

虽然可以通过修改数据库动态调整，但建议通过配置文件管理，便于版本控制和部署。

## 最佳实践

### 1. 任务命名规范

- 使用完整的模块路径作为任务名称
- 格式：`celery_tasks.beats.<模块名>.<任务函数名>`
- 示例：`celery_tasks.beats.business.send_daily_report`

### 2. 错误处理

定时任务应该包含完善的错误处理：

```python
@celery_app.task(bind=True, max_retries=3)
def unreliable_task(self):
    try:
        logger.info("执行可能失败的任务")
        # 可能失败的代码
    except Exception as exc:
        logger.error(f"任务失败：{exc}")
        # 自动重试
        raise self.retry(exc=exc, countdown=60)
```

### 3. 幂等性设计

定时任务应该具备幂等性，即使重复执行也不会产生副作用：

```python
@celery_app.task
def process_orders():
    # 只处理未处理的订单
    orders = Order.objects.filter(status='pending')
    for order in orders:
        process_single_order(order)
```

### 4. 日志记录

使用 Loguru 记录关键信息：

```python
logger.info("[定时任务] 开始执行")
logger.debug(f"处理数据：{data}")
logger.success("[定时任务] 执行成功")
logger.error(f"[定时任务] 执行失败：{error}")
```

### 5. 性能优化

- 避免在定时任务中执行耗时操作
- 对于大量数据处理，考虑拆分为多个子任务
- 使用异步任务处理 I/O 密集型操作

### 6. 监控告警

为关键任务添加监控：

```python
@celery_app.task
def critical_task():
    try:
        # 关键业务逻辑
        pass
    except Exception as e:
        # 发送告警通知
        send_alert_to_admin(f"关键任务失败：{e}")
        raise
```

## 常见问题

### Q1: Beat 启动了但任务没有执行？

**原因**: Worker 没有运行或任务路由错误

**解决方法**:

1. 确认 Worker 正在运行
2. 检查任务名称是否正确
3. 查看 Worker 日志是否有错误

### Q2: 如何查看定时任务的执行情况？

查看 Worker 的日志输出：

```bash
# Worker 日志会显示任务执行情况
2026-03-05 10:00:00 | INFO | "./celery_tasks/beats/example.py:18": print_time_task - [定时任务] 当前时间：2026-03-05 10:00:00
```

### Q3: Beat 的调度记录存储在哪里？

默认存储在本地文件中（如 `/var/folders/.../celerybeat-schedule`），重启后会保留调度状态。

### Q4: 如何在开发环境禁用某些定时任务？

方法 1: 在配置文件中注释掉对应任务

方法 2: 使用环境变量控制：

```python
if os.getenv('ENABLE_REPORT_TASK', 'true') == 'true':
    beat_schedule['send-daily-report'] = {...}
```

### Q5: 时区设置不生效怎么办？

确保以下配置正确：

1. `timezone` 设置为 `'Asia/Shanghai'`（或其他目标时区）
2. `enable_utc` 设置为 `False` 或与业务需求一致
3. `beat_scheduler_timezone` 与 `timezone` 保持一致

## 调试技巧

### 1. 测试单个任务

手动调用任务函数进行测试：

```python
from celery_tasks.beats.example import print_time_task

# 直接调用（同步）
result = print_time_task()
print(result)
```

### 2. 缩短执行间隔

在开发环境可以缩短任务的执行间隔：

```python
# 开发环境：每 10 秒执行一次
"test-task": {
    "task": "myapp.test_task",
    "schedule": 10.0,  # 生产环境改为 3600.0（1 小时）
}
```

### 3. 查看详细日志

提高日志级别以获取更多信息：

```bash
celery -A celery_tasks.beat beat --loglevel=debug
```

## 生产环境部署

### 1. 使用 systemd 管理（Linux）

创建服务文件 `/etc/systemd/system/celery-beat.service`：

```ini
[Unit]
Description=Celery Beat Service
After=network.target

[Service]
Type=forking
User=www-data
Group=www-data
WorkingDirectory=/path/to/project
ExecStart=/path/to/venv/bin/celery -A celery_tasks beat --loglevel=info
Restart=always

[Install]
WantedBy=multi-user.target
```

启动服务：

```bash
sudo systemctl start celery-beat
sudo systemctl enable celery-beat
```

### 2. 使用 Supervisor 管理

配置文件 `/etc/supervisor/conf.d/celery-beat.conf`：

```ini
[program:celery-beat]
command=/path/to/venv/bin/celery -A celery_tasks beat --loglevel=info
directory=/path/to/project
user=www-data
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/celery/beat.log
```

启动：

```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start celery-beat
```

### 3. Docker 部署

Dockerfile 示例：

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install celery redis

CMD celery -A celery_tasks worker --beat --loglevel=info
```

docker-compose.yml 示例：

```yaml
version: "3"
services:
  redis:
    image: redis:latest

  celery-worker:
    build: .
    command: celery -A celery_tasks worker --beat --loglevel=info
    depends_on:
      - redis
    volumes:
      - .:/app
```

## 参考资料

- [Celery Beat 官方文档](https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html)
- [Crondtab 语法说明](https://en.wikipedia.org/wiki/Cron)
- [Celery 任务配置最佳实践](https://docs.celeryq.dev/en/stable/userguide/configuration.html)

---

**相关文档**:

- [Celery Worker 异步任务使用指南](CELERY_WORKER_USAGE.md) - 异步任务执行
- [项目 README](../README.md) - 项目总体介绍
