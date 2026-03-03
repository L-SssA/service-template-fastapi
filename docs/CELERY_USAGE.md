# Celery 异步任务使用指南

## 目录结构

```
service-template-fastapi/
├── celery_tasks/              # Celery 任务模块
│   ├── __init__.py            # Celery 实例初始化和配置
│   ├── worker.py              # Worker 启动入口
│   ├── config.py              # Celery 配置加载
│   └── tasks/                 # 任务定义
│       ├── __init__.py
│       ├── example.py         # 示例任务（加法、睡眠）
│       └── logger_task.py     # 日志测试任务
├── app/
│   ├── routers/
│   │   └── celery.py          # Celery API 路由
│   ├── models/
│   │   └── celery.py          # Celery 数据模型
│   └── utils/
│       └── celery_client.py   # Celery 客户端工具
└── config.dev.toml            # Redis 和 Celery 配置
```

## 前置要求

### 1. 安装依赖

```bash
uv sync  # 或者 pip install -e .
```

确保已安装 `celery>=5.3.0` 和 `redis>=5.0.0`。

### 2. 启动 Redis 服务

**Windows (需要 WSL 或 Docker):**

```bash
docker run -d -p 6379:6379 redis:latest
```

**Linux:**

```bash
sudo systemctl start redis
```

**macOS:**

```bash
brew services start redis
```

## 快速开始

### 步骤 1: 启动 Celery Worker

在项目根目录下执行：

```bash
celery -A celery_tasks.worker worker --loglevel=info --pool=solo
```

**参数说明:**

- `-A celery_tasks.worker`: 指定 Celery 应用位置
- `--loglevel=info`: 日志级别
- `--pool=solo`: Windows 兼容模式（必须）

**成功输出示例:**

```
 -------------- celery@DESKTOP v5.3.0 (recovery)
--- ***** -----
-- ******* ---- Windows-10-10.0.22621-SP0 2026-03-03 10:00:00
- *** --- * ---
- ** ---------- [config]
- ** ---------- .> app:         celery_tasks:0x...
- ** ---------- .> broker:      redis://localhost:6379/0
- ** ---------- .> results:     redis://localhost:6379/1
- ** ---------- .> concurrency: 1 (solo)
- ** ---------- .> task events: off
- *** --- * --- [queues]
- ** ---------- .> celery           exchange=celery(direct) key=celery
```

### 步骤 2: 启动 FastAPI 应用

```bash
python main.py
```

如果检测到 Celery Worker，会显示：

```
2026-03-03 10:00:00 | SUCCESS | "./app/server.py:26": lifespan - 检测到 1 个活跃的 Celery Worker
```

### 步骤 3: 调用异步任务

#### 方式 1: 通过 API 接口（推荐）

访问 Swagger UI: http://127.0.0.1:8800/docs

可用的 Celery 端点：

1. **检查 Celery 状态**

   ```
   GET /celery/status
   ```

2. **创建加法任务**

   ```
   POST /celery/tasks/add
   Body: {"a": 10, "b": 20}
   ```

3. **创建睡眠任务**

   ```
   POST /celery/tasks/sleep
   Body: {"seconds": 5, "delay": 0}
   ```

4. **创建日志任务**

   ```
   POST /celery/tasks/log
   Body: {"level": "info", "message": "Test log"}
   ```

5. **查询任务状态**

   ```
   GET /celery/tasks/{task_id}
   ```

6. **取消/终止任务**
   ```
   DELETE /celery/tasks/{task_id}
   Body: {"terminate": false}  # true 表示强制终止正在运行的任务
   ```

#### 方式 2: 在代码中调用

```python
from app.utils.celery_client import send_task, get_task_result, get_task_status, revoke_task

# 发送异步任务
result = send_task(
    "celery_tasks.tasks.example.add_task",
    args=[10, 20]
)

print(f"Task ID: {result.id}")

# 获取结果（阻塞）
task_result = result.get(timeout=10)
print(f"Result: {task_result}")

# 或者先查状态，再获取结果
status = get_task_status(result.id)
if status == "SUCCESS":
    final_result = get_task_result(result.id)
elif status == "FAILURE":
    error = get_task_result(result.id)  # 获取异常信息
```

#### 方式 3: 使用便捷函数

```python
from app.utils.celery_client import (
    send_example_add_task,
    send_example_sleep_task,
    send_logger_task
)

# 快捷发送示例任务
result = send_example_add_task(100, 200)
print(result.get(timeout=10))  # 输出：300

# 快捷发送日志任务
send_logger_task("info", "这是一条测试日志")
```

### 连接性检查

`celery_client.py` 提供了连接性检查工具函数：

#### 1. `check_celery_connection()` - 详细检查

```python
from app.utils.celery_client import check_celery_connection

# 检查 Celery 连接状态
result = check_celery_connection(timeout=3)

if result["connected"]:
    print(f"✓ Redis 连接正常")
    print(f"✓ Worker 数量：{result['workers_count']}")
    if result["workers_count"] > 0:
        print(f"✓ Worker 列表：{list(result['workers'].keys())}")
else:
    print(f"✗ 连接失败：{result['error']}")
```

返回字典包含：

- `connected`: bool - 是否已连接
- `workers_count`: int - Worker 数量
- `workers`: dict - Worker 详细信息
- `error`: str - 错误信息（如果有）

#### 2. `is_celery_available()` - 快速检查

```python
from app.utils.celery_client import is_celery_available

# 快速检查 Celery 是否可用
if is_celery_available():
    # Celery 可用，发送任务
    result = send_task("my_task", args=[1, 2])
else:
    logger.warning("Celery 不可用，跳过异步任务")
```

这些检查函数会在应用启动时自动执行（在 `app/server.py` 的 lifespan 中），你也可以在其他地方手动调用。

## 内置任务示例

### 1. 加法任务 (add_task)

位置：`celery_tasks.tasks.example.add_task`

```python
from app.utils.celery_client import send_example_add_task

result = send_example_add_task(100, 200)
print(result.get(timeout=10))  # 输出：300
```

或者使用通用方法：

```python
from app.utils.celery_client import send_task

result = send_task(
    "celery_tasks.tasks.example.add_task",
    args=[100, 200]
)
print(result.get(timeout=10))  # 输出：300
```

### 2. 睡眠任务 (sleep_task)

位置：`celery_tasks.tasks.example.sleep_task`

```python
from app.utils.celery_client import send_example_sleep_task

# 立即执行，睡眠 5 秒
result = send_example_sleep_task(5)

# 延迟 10 秒后执行，睡眠 5 秒
result = send_example_sleep_task(5, countdown=10)
```

参数说明：

- `seconds`: 睡眠秒数
- `countdown`: 延迟执行时间（可选）

### 3. 日志任务 (log_message)

位置：`celery_tasks.tasks.logger_task.log_message`

```python
from app.utils.celery_client import send_logger_task

# 测试不同级别的日志
send_logger_task("debug", "这是一条调试日志")
send_logger_task("info", "这是一条信息日志")
send_logger_task("success", "这是一条成功日志")
send_logger_task("warning", "这是一条警告日志")
send_logger_task("error", "这是一条错误日志")
```

支持的日志级别：`debug`, `info`, `success`, `warning`, `error`

### 4. 多级别日志批量测试 (multi_level_logs)

位置：`celery_tasks.tasks.logger_task.multi_level_logs`

```python
from app.utils.celery_client import send_task

# 生成多条多级别日志
result = send_task(
    "celery_tasks.tasks.logger_task.multi_level_logs",
    args=[5]  # 每种级别生成 5 条
)
print(result.get(timeout=10))
```

这个任务会循环生成 DEBUG, INFO, SUCCESS, WARNING, ERROR 各 5 条日志，用于测试日志系统。

## 高级用法

### 1. 任务路由和队列

```python
# 发送到特定队列
result = send_task(
    "celery_tasks.tasks.example.add_task",
    args=[1, 2],
    queue="high_priority"
)
```

### 2. 任务超时和重试

```python
# 设置任务超时
result = send_task(
    "celery_tasks.tasks.example.sleep_task",
    args=[10],
    time_limit=5  # 5 秒后强制终止
)

# 设置延迟执行
result = send_task(
    "celery_tasks.tasks.example.add_task",
    args=[1, 2],
    countdown=60  # 60 秒后执行
)

# 设置定时执行
from datetime import datetime, timedelta
eta_time = datetime.now() + timedelta(minutes=5)
result = send_task(
    "celery_tasks.tasks.example.add_task",
    args=[1, 2],
    eta=eta_time
)
```

### 3. 任务撤销

```python
from app.utils.celery_client import revoke_task

# 撤销未开始的任务
revoke_task(task_id)

# 终止正在运行的任务（发送 SIGTERM 信号）
revoke_task(task_id, terminate=True)

# 使用其他信号（如 SIGKILL）
revoke_task(task_id, terminate=True, signal='SIGKILL')
```

注意：

- `terminate=False` 时，任务会在完成当前任务后不再执行
- `terminate=True` 时，会强制终止正在运行的任务
- 默认信号是 `SIGTERM`，可以使用 `signal` 参数指定其他信号

### 4. 批量任务

```python
from celery_tasks import celery_app
from celery import group

# 使用 group 批量执行相同类型的任务
task_group = group(
    celery_app.send_task("celery_tasks.tasks.example.add_task", args=[i, i+1])
    for i in range(10)
)
results = task_group.apply_async()

# 等待所有任务完成
all_results = results.get(timeout=30)
print(f"所有任务结果：{all_results}")
```

### 5. 自定义任务参数

```python
from app.utils.celery_client import send_task

# 使用 kwargs 传递参数
result = send_task(
    "celery_tasks.tasks.logger_task.log_message",
    kwargs={"level": "info", "message": "测试消息"}
)

# 混合使用 args 和 kwargs
result = send_task(
    "celery_tasks.tasks.example.add_task",
    args=[10],
    kwargs={"b": 20}  # 如果任务支持的话
)
```

## 配置说明

### config.dev.toml

```toml
[redis]
host = "localhost"
port = 6379
db = 0
password = ""

[celery]
broker_url = "redis://localhost:6379/0"
result_backend = "redis://localhost:6379/1"
task_serializer = "json"
result_serializer = "json"
accept_content = ["json"]
timezone = "Asia/Shanghai"
enable_utc = true
```

### 环境变量

可以通过环境变量切换配置：

```bash
# Windows PowerShell
$env:ENV="prod"
python main.py
celery -A celery_tasks.worker worker --loglevel=info --pool=solo

# Linux/macOS
export ENV=prod
python main.py
celery -A celery_tasks.worker worker --loglevel=info
```

支持的环境：

- `dev` (默认): 使用 `config.dev.toml`
- `prod`: 使用 `config.prod.toml`（需要自行创建）
- 其他自定义环境：使用 `config.{env}.toml`

## 日志系统

Celery 任务中的日志与主应用保持一致的格式：

```
2026-03-03 10:00:00 | INFO | "./celery_tasks/tasks/example.py:21": add_task - 执行加法任务：10 + 20
2026-03-03 10:00:00 | SUCCESS | "./celery_tasks/tasks/example.py:23": add_task - 加法任务完成，结果：30
```

特点：

- ✅ 使用相对路径（相对于项目根目录）
- ✅ 相同等级着色（INFO=白色，SUCCESS=绿色，ERROR=红色等）
- ✅ 统一的格式样式
- ✅ 支持多种日志级别：DEBUG, INFO, SUCCESS, WARNING, ERROR

### 日志级别颜色说明

- `DEBUG`: 调试信息（灰色）
- `INFO`: 一般信息（白色）
- `SUCCESS`: 成功信息（绿色）
- `WARNING`: 警告信息（黄色）
- `ERROR`: 错误信息（红色）

## 常见问题

### Q1: Worker 无法启动

**问题**: `Error: No module named 'celery'`

**解决**:

```bash
uv sync  # 确保安装了依赖
```

### Q2: Redis 连接失败

**问题**: `Error: Connection to Redis failed`

**解决**:

1. 确认 Redis 服务已启动
2. 检查 `config.dev.toml` 中的 Redis 地址是否正确
3. 测试 Redis 连接：`redis-cli ping`

### Q3: 任务一直处于 PENDING 状态

**原因**: Worker 未启动或任务路由错误

**解决**:

1. 确认 Worker 正在运行
2. 检查任务名称是否正确（使用完整路径如 `celery_tasks.tasks.example.add_task`）
3. 查看 Worker 日志是否有错误
4. 检查 Redis 连接是否正常

### Q4: Windows 下多进程问题

**问题**: `UserWarning: Starting from a new process...`

**解决**: 必须使用 `--pool=solo` 参数：

```bash
celery -A celery_tasks.worker worker --loglevel=info --pool=solo
```

原因：Windows 不支持 fork 多进程，只能使用 solo 模式（单进程）。

### Q5: 任务执行失败如何获取错误信息

**方法**:

```python
from app.utils.celery_client import get_task_result, get_task_status

task_id = "your-task-id"
status = get_task_status(task_id)

if status == "FAILURE":
    try:
        error = get_task_result(task_id)
        print(f"任务失败：{error}")
    except Exception as e:
        print(f"获取错误失败：{e}")
```

或者通过 API 接口查询，返回中会包含 `error` 字段。

## 最佳实践

1. **任务幂等性**: 确保任务可以安全重试，避免重复执行产生副作用
2. **任务超时**: 为长时间运行的任务设置 `time_limit` 和 `soft_time_limit`
3. **错误处理**: 在任务中添加适当的异常捕获和日志记录
4. **日志记录**: 使用 Loguru 记录关键步骤，便于问题排查
5. **监控告警**: 定期检查任务失败率，设置告警阈值
6. **资源清理**: 任务完成后释放数据库连接、文件句柄等资源
7. **任务拆分**: 将大任务拆分为小任务，提高并发性和可维护性
8. **结果过期**: 合理设置 `result_expires`，避免 Redis 内存占用过高
9. **优先级队列**: 对重要任务使用独立队列，确保及时处理
10. **任务限流**: 使用 `rate_limit` 限制任务执行频率，保护下游服务

## 扩展开发

### 添加新任务

在 `celery_tasks/tasks/` 目录下创建新文件：

```python
# celery_tasks/tasks/my_task.py
from loguru import logger
from celery_tasks import celery_app


@celery_app.task(name="celery_tasks.tasks.my_task.process_data")
def process_data(data: dict) -> dict:
    """
    数据处理任务

    Args:
        data: 待处理的数据字典

    Returns:
        处理结果
    """
    logger.info(f"开始处理数据：{data}")

    # 业务逻辑
    result = {"processed": True, "data": data}

    logger.success(f"数据处理完成")
    return result
```

然后在 `celery_tasks/tasks/__init__.py` 中导入：

```python
# celery_tasks/tasks/__init__.py
from . import example
from . import logger_task
from . import my_task  # 新增
```

### 添加新的 API 端点

在 `app/routers/celery.py` 中添加新的路由：

```python
@router.post("/tasks/custom", summary="创建自定义任务", response_model=TaskResponse)
async def create_custom_task(request: CustomTaskRequest):
    result = send_task(
        request.task_name,
        args=request.args,
        kwargs=request.kwargs
    )

    return TaskResponse(
        code=200,
        data=TaskData(
            task_id=result.id,
            status="pending",
        ),
        message=f"Custom task created: {request.task_name}"
    )
```

同时在 `app/models/celery.py` 中添加对应的请求模型。

## 下一步

- [ ] 实现定时任务 (Celery Beat)
- [ ] 添加任务监控面板（如 Flower）
- [ ] 实现任务优先级队列
- [ ] 添加任务重试机制和死信队列
- [ ] 集成任务执行时间统计
- [ ] 添加任务依赖关系支持
