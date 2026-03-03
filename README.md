# FastAPI 开发模板

## 介绍

这是一个基于 FastAPI 框架的现代化 Web 服务开发模板，提供了完整的项目结构和最佳实践配置。

### 技术栈

- **核心框架**: [FastAPI](https://fastapi.tiangolo.com/zh/) - 现代、快速（高性能）的 Web 框架
- **ASGI 服务器**: [Uvicorn](https://www.uvicorn.org/) - 闪电般快速的 ASGI 服务器
- **日志系统**: [Loguru](https://github.com/Delgan/loguru) - 简化 Python 日志记录
- **配置管理**: [TOML](https://github.com/uiri/toml) - 简洁易读的配置文件格式
- **异步任务**: [Celery](https://docs.celeryq.dev/) + [Redis](https://redis.io/) - 分布式任务队列
- **类型提示**: 完整的 Pydantic 模型支持

## 项目结构

```
service-template-fastapi/
├── app/                    # 应用核心代码
│   ├── config/            # 配置管理
│   │   └── config.py      # 主配置文件
│   ├── models/            # 数据模型定义
│   │   ├── base.py        # 基础模型
│   │   ├── celery.py      # Celery 任务模型
│   │   ├── example.py     # 示例模型
│   │   ├── exception.py   # 异常处理模型
│   │   └── system.py      # 系统管理模型
│   ├── routers/           # API 路由
│   │   ├── __init__.py    # 路由聚合
│   │   ├── base.py        # 路由基础类
│   │   ├── celery.py      # Celery 任务路由
│   │   ├── example.py     # 示例路由
│   │   └── system.py      # 系统管理路由
│   ├── utils/             # 工具函数
│   │   ├── celery_client.py  # Celery 客户端
│   │   ├── decorators.py  # 装饰器
│   │   ├── http_utils.py  # HTTP 工具
│   │   ├── logger.py      # 日志配置
│   │   ├── server.py      # 服务器工具
│   │   ├── sys_utils.py   # 系统工具
│   │   └── tools.py       # 通用工具
│   └── server.py          # FastAPI 应用实例
├── celery_tasks/          # Celery 异步任务模块
│   ├── __init__.py        # Celery 实例初始化
│   ├── worker.py          # Worker 启动入口
│   ├── config.py          # Celery 配置
│   └── tasks/             # 任务定义
│       ├── __init__.py
│       ├── example.py     # 示例任务
│       └── logger_task.py # 日志测试任务
├── public/                # 静态资源
│   └── index.html         # 默认首页
├── docs/                  # 文档目录
│   └── CELERY_USAGE.md    # Celery 使用指南
├── scripts/               # 脚本目录
│   └── start_celery_worker.bat  # Worker 启动脚本 (Windows)
├── config.dev.toml        # 开发环境配置
├── main.py                # 应用入口文件
├── pyproject.toml         # 项目配置和依赖
└── uv.lock                # UV 锁定文件
```

## 快速开始

### 前置要求

#### 1. Redis 服务

Celery 需要 Redis 作为消息代理。可以使用 Docker 快速启动：

```bash
docker run -d -p 6379:6379 redis:latest
```

或使用本地安装的 Redis 服务。

### 环境要求

- Python >= 3.10
- pip 或 uv 包管理器

### 安装依赖

使用 pip 安装：

```bash
pip install -r requirements.txt
```

或使用 uv（推荐）：

```bash
uv sync
```

### 运行项目

**步骤 1: 启动 Celery Worker** (新终端窗口)

```bash
# Windows
.\start_celery_worker.bat

# Linux/macOS
celery -A celery_tasks.worker worker --loglevel=info --pool=solo
```

**步骤 2: 启动 FastAPI 应用**

```bash
# 设置环境变量并运行
ENV=dev python main.py

# 或直接运行（默认 dev 环境）
python main.py
```

如果 Worker 已启动，应用会显示：`检测到 X 个活跃的 Celery Worker`

#### 生产模式

```bash
# 设置生产环境
ENV=prod python main.py
```

### 访问接口文档

项目启动后，可以通过以下地址访问自动生成的 API 文档：

- **Swagger UI**: http://localhost:8800/docs
- **ReDoc**: http://localhost:8800/redoc

### 接口分类说明

项目采用模块化路由设计，主要接口分类如下：

- **`/example/*`**: 示例接口
- **`/celery/*`**: Celery 异步任务创建接口（加法、睡眠、日志测试等）
- **`/tasks/*`**: 通用任务管理接口（状态查询、任务取消等）
- **`/system/*`**: 系统管理接口（服务健康检查、组件状态监控等）

## 配置说明

### 项目配置 (pyproject.toml)

```toml
[project]
name = "service-template"
version = "0.1.0"
description = "一个 fastapi 的开发模板"
requires-python = ">=3.10"
dependencies = [
    "fastapi>=0.123.10",
    "loguru>=0.7.3",
    "toml>=0.10.2",
    "uvicorn>=0.38.0",
    "celery>=5.3.0",
    "redis>=5.0.0",
]
```

### 环境配置 (config.{env}.toml)

开发环境配置示例：

```toml
[service]
listen_host = "0.0.0.0"    # 监听地址
listen_port = 8800         # 监听端口
log_level = "debug"        # 日志级别
reload_debug = false       # 是否开启热重载

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

## API 示例

### 示例接口

POST `/example/` - 示例接口

请求体：

```json
{
  "id": 1,
  "name": "test"
}
```

响应：

```json
{
  "code": 200,
  "message": "操作成功",
  "data": null
}
```

## 核心特性

### 🔧 统一异常处理

通过装饰器实现统一的异常捕获和响应格式

### 📝 结构化日志

使用 Loguru 提供清晰的日志输出和管理，支持多种日志级别（DEBUG, INFO, SUCCESS, WARNING, ERROR）

### ⚙️ 灵活配置

支持多环境配置（dev/prod），基于 TOML 文件和环境变量切换

### 🛠️ 工具集成

内置常用的工具函数和装饰器，包括：

- Celery 客户端工具（发送任务、查询状态、获取结果）
- HTTP 工具（统一响应格式）
- 系统工具（路径处理、文件操作）
- 装饰器（异常处理装饰器）

### 📚 自动文档

自动生成交互式 API 文档，支持 Swagger UI 和 ReDoc

### 🔄 异步任务队列

基于 Celery + Redis 的完整异步任务解决方案，支持：

- ✅ 分布式任务执行
- ✅ 任务状态追踪（PENDING, STARTED, RETRY, SUCCESS, FAILURE）
- ✅ 延迟任务和定时任务
- ✅ 任务重试机制
- ✅ 统一日志输出
- ✅ 任务取消/终止功能

## 异步任务

本项目集成了 Celery 提供异步任务处理能力。详细使用指南请参考 [docs/CELERY_USAGE.md](docs/CELERY_USAGE.md)。

### 快速开始

1. **启动 Redis**:

   ```bash
   docker run -d -p 6379:6379 redis:latest
   ```

2. **启动 Celery Worker** (新终端窗口):

   ```bash
   .\start_celery_worker.bat  # Windows
   celery -A celery_tasks.worker worker --loglevel=info --pool=solo  # Linux/macOS
   ```

3. **启动 FastAPI 应用**:

   ```bash
   python main.py
   ```

4. **调用异步任务**:
   - 访问 Swagger UI: http://localhost:8800/docs
   - 查看 `/celery/*` 端点（创建任务）
   - 查看 `/tasks/*` 端点（任务管理）
   - 或在代码中使用 `app.utils.celery_client.send_task()`

### 内置任务示例

- `add_task`: 简单的加法任务（测试用）
- `sleep_task`: 延迟响应测试（可设置睡眠秒数和延迟执行）
- `log_message`: 日志测试任务（支持多种日志级别）
- `multi_level_logs`: 多级别日志批量测试任务

### 测试集成

运行集成测试验证 Celery 是否正常工作：

```bash
python test_celery_integration.py
```

## 开发指南

### 添加新路由

1. 在 `app/routers/` 目录下创建新的路由文件
2. 使用 `create_router()` 函数创建路由实例（自动设置 prefix 和 tags）
3. 在 `app/routers/__init__.py` 中导入并注册到 `root_router`
4. 路由会自动在 `app/server.py` 中被包含

示例：

```python
# app/routers/my_router.py
from app.routers.base import create_router

router = create_router("my_prefix")

@router.get("/endpoint")
async def my_endpoint():
    return {"message": "Hello"}
```

```python
# app/routers/__init__.py
from .my_router import router as my_router

root_router.include_router(my_router)
```

### 添加数据模型

1. 在 `app/models/` 目录下创建模型文件
2. 继承 `IBaseModel`（请求模型）或 `BaseResponse`（响应模型）定义 Pydantic 模型
3. 在路由中使用类型注解

示例：

```python
# app/models/my_model.py
from app.models.base import IBaseModel, BaseResponse

class MyRequest(IBaseModel):
    name: str
    age: int

class MyData(IBaseModel):
    result: str

class MyResponse(BaseResponse):
    data: MyData
```

### 自定义工具函数

在 `app/utils/` 目录下添加相应的工具模块，常用工具包括：

- `celery_client.py`: Celery 任务客户端（发送任务、查询状态、获取结果、撤销任务）
- `decorators.py`: 装饰器（如 `@exception_handler` 用于统一异常处理）
- `http_utils.py`: HTTP 工具（生成统一响应格式）
- `logger.py`: 日志配置和初始化工具
- `server.py`: 服务器相关工具（错误处理器）
- `sys_utils.py`: 系统工具（路径处理、文件操作）
- `tools.py`: 通用工具（TOML 文件加载等）

## 部署建议

### 生产环境配置

创建 `config.prod.toml`：

```toml
[service]
listen_host = "0.0.0.0"
listen_port = 8000
log_level = "info"
reload_debug = false
```

### Docker 部署

```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY . .
RUN pip install uv && uv sync --frozen

EXPOSE 8000
CMD ["python", "main.py"]
```

或者使用多阶段构建（包含 Celery Worker）：

```dockerfile
FROM python:3.10-slim as base

WORKDIR /app
COPY . .
RUN pip install uv && uv sync --frozen

# FastAPI 服务
FROM base as api
EXPOSE 8000
CMD ["python", "main.py"]

# Celery Worker
FROM base as worker
CMD ["celery", "-A", "celery_tasks.worker", "worker", "--loglevel=info"]
```

## 贡献指南

欢迎提交 Issue 和 Pull Request 来改进这个模板！

## 许可证

MIT License
