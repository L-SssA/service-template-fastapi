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
│   ├── modules/           # 业务模块
│   │   └── module_name/
│   │       ├── __init__.py # 模块初始化
│   │       ├── models.py  # 数据模型定义
│   │       ├── routes.py  # 路由定义
│   │       ├── schemas.py # 数据结构定义
│   │       └── service.py # 业务逻辑
│   ├── shared/            # 公共接口和数据结构
│   │   ├── exception_schemas.py # 异常响应模型
│   │   ├── routes.py      # 公共路由
│   │   └── schemas.py     # 公共请求和响应模型
│   ├── utils/             # 工具函数
│   │   ├── celery_client.py  # Celery 客户端
│   │   ├── decorators.py  # 装饰器
│   │   ├── http_utils.py  # HTTP 工具
│   │   ├── logger.py      # 日志配置
│   │   ├── server.py      # 服务器工具
│   │   ├── sys_utils.py   # 系统工具
│   │   └── tools.py       # 通用工具
│   ├── db.py              # 数据库相关功能
│   ├── routers.py         # 路由聚合
│   └── server.py          # FastAPI 应用实例
├── celery_tasks/          # Celery 异步任务模块
│   ├── __init__.py        # Celery 模块初始化
│   ├── celery_app.py      # Celery 实例和应用配置
│   ├── config.py          # Celery 配置和定时任务配置
│   ├── tasks/             # 异步任务定义
│   │   ├── __init__.py
│   │   ├── example.py     # 示例任务
│   │   └── logger_task.py # 日志测试任务
│   └── beats/             # 定时任务定义 ⭐
│       ├── __init__.py
│       ├── business.py    # 业务定时任务
│       └── example.py     # 示例定时任务
├── public/                # 静态资源
│   └── index.html         # 默认首页
├── docs/                  # 文档目录
│   ├── BEAT_QUICKSTART.md         # Beat 快速入门
│   ├── CELERY_BEAT_USAGE.md      # Celery Beat 使用指南
│   └── CELERY_WORKER_USAGE.md    # Celery Worker 使用指南
├── scripts/               # 脚本目录
│   └── start_celery.py    # Celery 统一启动脚本（跨平台）
├── config.dev.toml        # 开发环境配置
├── main.py                # 应用入口文件
├── pyproject.toml         # 项目配置和依赖
└── uv.toml                # uv 工具配置
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
# Windows/Linux/macOS 统一使用 Python 脚本
uv run python scripts/start_celery.py worker

# 或者使用原生命令（不推荐）
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
- **定时任务**: Celery Beat 自动执行（日报、备份、清理等） ⭐

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

### 🔥 定时任务 (Celery Beat) ⭐

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
# 方式 1: Worker + Beat 一体化（推荐，开发测试环境）
uv run python scripts/start_celery.py all  # 跨平台统一命令

# 方式 2: 分别启动 Worker 和 Beat（生产环境推荐）
uv run python scripts/start_celery.py worker &  # Worker
uv run python scripts/start_celery.py beat      # Beat（新终端）
```

详细使用指南请参考 [docs/CELERY_BEAT_USAGE.md](docs/CELERY_BEAT_USAGE.md)。

## 异步任务

本项目集成了 Celery 提供异步任务处理能力。

### 快速开始

1. **启动 Redis**:

   ```bash
   docker run -d -p 6379:6379 redis:latest
   ```

2. **启动 Celery Worker** (新终端窗口):

   ```bash
   # Windows/Linux/macOS 统一使用 Python 脚本
   uv run python scripts/start_celery.py worker
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

### 详细文档

- **[Celery Worker 使用指南](docs/CELERY_WORKER_USAGE.md)** - 异步任务执行、配置和最佳实践
- **[Celery Beat 定时任务使用指南](docs/CELERY_BEAT_USAGE.md)** - 定时任务调度和管理

## 下一步

### 已完成的功能

- [x] 实现定时任务 (Celery Beat) ⭐

### 计划中的功能

- [ ] 添加任务监控面板（如 Flower）
- [ ] 实现任务优先级队列
- [ ] 添加任务重试机制和死信队列
- [ ] 集成任务执行时间统计
- [ ] 添加任务依赖关系支持

---

## 贡献指南

欢迎提交 Issue 和 Pull Request 来改进这个模板！

## 许可证

MIT License
