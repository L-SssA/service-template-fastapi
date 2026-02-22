# FastAPI 开发模板

## 介绍

这是一个基于 FastAPI 框架的现代化 Web 服务开发模板，提供了完整的项目结构和最佳实践配置。

### 技术栈

- **核心框架**: [FastAPI](https://fastapi.tiangolo.com/zh/) - 现代、快速（高性能）的 Web 框架
- **ASGI 服务器**: [Uvicorn](https://www.uvicorn.org/) - 闪电般快速的 ASGI 服务器
- **日志系统**: [Loguru](https://github.com/Delgan/loguru) - 简化 Python 日志记录
- **配置管理**: [TOML](https://github.com/uiri/toml) - 简洁易读的配置文件格式
- **类型提示**: 完整的 Pydantic 模型支持

## 项目结构

```
service-template-fastapi/
├── app/                    # 应用核心代码
│   ├── config/            # 配置管理
│   │   ├── __init__.py
│   │   └── config.py      # 主配置文件
│   ├── models/            # 数据模型定义
│   │   ├── __init__.py
│   │   ├── base.py        # 基础模型
│   │   ├── example.py     # 示例模型
│   │   └── exception.py   # 异常处理模型
│   ├── routers/           # API 路由
│   │   ├── __init__.py
│   │   ├── base.py        # 路由基础类
│   │   └── example.py     # 示例路由
│   ├── utils/             # 工具函数
│   │   ├── __init__.py
│   │   ├── decorators.py  # 装饰器
│   │   ├── http_utils.py  # HTTP 工具
│   │   ├── logger.py      # 日志配置
│   │   ├── server.py      # 服务器工具
│   │   ├── sys_utils.py   # 系统工具
│   │   └── tools.py       # 通用工具
│   └── server.py          # FastAPI 应用实例
├── public/                # 静态资源
│   └── index.html         # 默认首页
├── config.dev.toml        # 开发环境配置
├── main.py               # 应用入口文件
├── pyproject.toml        # 项目配置和依赖
└── uv.toml              # UV 工具配置
```

## 快速开始

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

#### 开发模式
```bash
# 设置环境变量并运行
ENV=dev python main.py

# 或直接运行（默认 dev 环境）
python main.py
```

#### 生产模式
```bash
# 设置生产环境
ENV=prod python main.py
```

### 访问接口文档

项目启动后，可以通过以下地址访问自动生成的 API 文档：

- **Swagger UI**: http://localhost:8800/docs
- **ReDoc**: http://localhost:8800/redoc

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
使用 Loguru 提供清晰的日志输出和管理

### ⚙️ 灵活配置
支持多环境配置，易于部署到不同环境

### 🛠️ 工具集成
内置常用的工具函数和装饰器，提高开发效率

### 📚 自动文档
自动生成交互式 API 文档，支持 Swagger 和 ReDoc

## 开发指南

### 添加新路由

1. 在 `app/routers/` 目录下创建新的路由文件
2. 使用 `create_router()` 函数创建路由实例
3. 在 `app/server.py` 中注册路由

### 添加数据模型

1. 在 `app/models/` 目录下创建模型文件
2. 继承 Pydantic BaseModel 定义请求/响应模型
3. 在路由中使用类型注解

### 自定义工具函数

在 `app/utils/` 目录下添加相应的工具模块。

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
RUN pip install -r requirements.txt

EXPOSE 8000
CMD ["python", "main.py"]
```

## 贡献指南

欢迎提交 Issue 和 Pull Request 来改进这个模板！

## 许可证

MIT License