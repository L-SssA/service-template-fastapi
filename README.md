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
├── app/                           # 应用核心代码
│   ├── config.py                  # 环境变量、项目配置与全局参数读取
│   ├── exceptions.py              # 全局异常处理注册
│   ├── middlewares.py             # 中间件注册
│   ├── routers.py                 # 自动扫描 app/modules 中的 routes.py 并装配 root_router
│   ├── server.py                  # FastAPI 实例、life_span 与静态资源挂载
│   ├── db/                        # 数据库与 Redis 连接能力
│   ├── modules/                   # 业务模块
│   │   └── module_name/
│   │       ├── __init__.py
│   │       ├── models.py         # 数据库模型
│   │       ├── routes.py         # 路由定义
│   │       ├── schemas.py        # 数据结构定义
│   │       └── service.py        # 业务逻辑
│   ├── shared/                    # 公共接口、基类、路由工厂等共享能力
│   └── utils/                     # 工具函数
├── celery_app/                    # Celery 应用包
│   ├── config.py                  # Celery 配置与 Beat schedule
│   ├── server.py                  # Celery 实例创建与自动加载任务
│   └── tasks/                     # 任务定义
├── migrations/                    # Alembic 数据库迁移目录
├── public/                        # 静态资源目录
├── docs/                          # 文档目录
├── scripts/                       # 脚本目录
├── tests/                         # 测试目录
├── config.dev.toml                # 开发环境配置
├── config.example.toml            # 配置示例文件
├── main.py                         # 入口文件：拉起 FastAPI 与 Celery Worker/Beat
├── api_server.py                  # 仅启动 FastAPI 服务的部署入口
├── celery_server.py               # 仅启动 Celery Worker/Beat 的部署入口
├── Dockerfile                     # 容器镜像构建文件
├── docker-compose.yml             # 本地/部署编排文件
├── pyproject.toml                 # 项目配置和依赖
└── uv.toml                         # uv 工具配置
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

优先使用 uv（推荐）：

```bash
uv sync
```

如果你希望用传统 pip 方式安装，也可以基于项目 `pyproject.toml` 手动构建环境：

```bash
pip install -e .
```

### 运行项目

项目默认同时启动 FastAPI 服务与 Celery Worker/Beat 进程；在 Windows 平台下会单独创建 Worker 和 Beat 进程，在类 Unix 平台下会以一个 Celery 进程同时承载 Worker + Beat。

```bash
# 一条命令启动应用与 Celery
uv run python main.py
```

如果 Redis 和 Celery Worker 已就绪，应用启动时会通过 `app.utils.celery_client` 检查连接并打印：`检测到 X 个活跃的 Celery Worker`。

#### 独立部署入口

仓库额外提供了两个独立部署入口：

```bash
# 单独启动 API 服务
uv run python api_server.py

# 单独启动 Celery Worker + Beat
uv run python celery_server.py
```

这两种入口适合在容器化部署或当需要把 API 与任务处理拆开部署时使用。

#### 生产模式

```bash
# 通过环境变量切换配置文件，例如：ENV=prod
ENV=prod uv run python main.py
```

### Docker Compose 部署

项目根目录已经包含 `Dockerfile` 与 `docker-compose.yml`，可直接通过容器编排方式拉起 Redis、Postgres、FastAPI API 和 Celery 服务：

```bash
docker compose up --build
```

其中：

- `redis`：消息代理与任务结果缓存
- `postgres`：主数据库服务
- `api_server`：统一的 FastAPI 服务
- `celery_server`：独立 Celery Worker/Beat 任务服务

### 访问接口文档

项目启动后，可以通过以下地址访问自动生成的 API 文档：

- **Swagger UI**: http://localhost:8800/docs
- **ReDoc**: http://localhost:8800/redoc

## 配置说明

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

### 🔥 定时任务 (Celery Beat)

基于 Celery Beat 的定时任务调度器，支持：

- ✅ Crontab 表达式（每小时、每天、每周等）
- ✅ 固定间隔执行（每 N 秒/分钟）
- ✅ 丰富的任务类型（日报、备份、清理、同步等）
- ✅ 统一的日志输出和错误处理
- ✅ 灵活的调度配置

内置定时任务示例：

| 任务名称   | 功能说明           | 执行频率   |
| ---------- | ------------------ | ---------- |
| 打印时间   | 每分钟打印当前时间 | 每 60 秒   |
| 清理会话   | 清理过期用户会话   | 每 30 分钟 |
| 数据同步   | 同步外部数据       | 每小时整点 |
| 统计计算   | 计算实时统计数据   | 每 15 分钟 |
| 发送日报   | 生成并发送每日报告 | 每天 18:00 |
| 数据库备份 | 执行数据库备份     | 每天 02:00 |

**启动定时任务:**

```bash
# 推荐方式：直接用主入口启动，Celery 进程会按平台自动拉起 Worker/Beat
uv run python main.py
```

## 异步任务

本项目集成了 Celery 提供异步任务处理能力。

### 快速开始

1. **启动 Redis**:

   ```bash
   docker run -d -p 6379:6379 redis:latest
   ```

2. **启动 FastAPI 与 Celery 进程**:

   ```bash
   uv run python main.py
   ```

3. **调用异步任务**:
   - 访问 Swagger UI: http://localhost:8800/docs
   - 查看 `/celery/*` 端点（创建任务）
   - 查看 `/tasks/*` 端点（任务管理）
   - 或在代码中使用 `from app.utils.celery_client import celery_client`，再通过 `celery_client.send_task(...)` 发起任务

## 贡献指南

欢迎提交 Issue 和 Pull Request 来改进这个模板！

## 许可证

MIT License