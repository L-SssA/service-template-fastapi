# 项目开发指南 (AGENTS.md)

本文档记录了项目的设计原则和开发规范，所有参与开发的 AI 助手和开发人员都应遵循这些约定。

## 📁 一、项目结构设计

### 1.1 目录结构规范

项目采用模块化设计，代码应按照以下目录结构组织：

```
service-template-fastapi/
├── app/                    # 应用核心代码
│   ├── config/            # 配置管理
│   ├── models/            # 数据模型定义 ⭐
│   ├── routers/           # API 路由 ⭐
│   ├── utils/             # 工具函数
│   └── server.py          # FastAPI 应用实例
├── celery_tasks/          # Celery 异步任务模块 ⭐
├── docs/                  # 文档目录 ⭐
├── public/                # 静态资源
├── scripts/               # 脚本目录
└── 配置文件
```

### 1.2 关键目录说明

- **`app/models/`**: 存放所有数据模型定义
- **`app/routers/`**: 存放所有 API 路由，按模块分文件编写
- **`celery_tasks/`**: 存放所有异步任务定义
- **`docs/`**: 存放所有项目文档（除 README.md 外）

---

## 🏗️ 二、数据模型规范

### 2.1 模型分类

所有数据模型必须放在 `app/models/` 目录下，并遵循以下继承规则：

#### Request 模型（请求体）

- **必须继承自 `IBaseModel`**
- 用于定义 API 请求的数据结构
- 支持自动字符串截断和格式化输出

```python
# app/models/example.py
from app.models.base import IBaseModel

class UserRequest(IBaseModel):
    """用户请求模型"""
    username: str
    email: str
    age: int | None = None
```

#### Response 模型（响应体）

- **必须继承自 `BaseResponse`**
- 用于定义 API 响应的数据结构
- 自动包含 `code`, `data`, `message` 字段

```python
# app/models/example.py
from typing import Any, Optional
from app.models.base import BaseResponse

class UserData(IBaseModel):
    """用户数据模型"""
    user_id: int
    username: str
    email: str

class UserResponse(BaseResponse):
    """用户响应模型"""
    data: UserData | None = None
```

### 2.2 基类说明

**IBaseModel** (`app/models/base.py`)

- 继承自 `pydantic.BaseModel`
- 提供 `__trim_string__()` 方法：自动截断过长的字符串（最大 200 字符）
- 重写 `__repr_args__()` 方法：优化调试输出

**BaseResponse** (`app/models/base.py`)

- 继承自 `IBaseModel`
- 标准响应格式：
  ```python
  {
      "code": 200,           # 状态码
      "data": Any,           # 响应数据
      "message": "操作成功"  # 响应消息
  }
  ```

### 2.3 模型文件命名

- 使用小写字母和下划线：`user_model.py`, `order_model.py`
- 或在 `example.py` 中按功能分组定义多个相关模型
- 每个模型类应包含清晰的文档字符串

---

## 🛣️ 三、路由开发规范

### 3.1 模块化路由

**原则**: 除非特殊情况，routers 应该分模块编写

#### 步骤 1: 创建路由文件

在 `app/routers/` 目录下创建新的路由文件，以模块名命名：

```python
# app/routers/user.py
from fastapi import APIRouter
from app.routers.base import create_router

# 使用 create_router 创建路由实例
router = create_router("user")

@router.get("/{user_id}")
async def get_user(user_id: int):
    """获取用户信息"""
    return {"user_id": user_id}

@router.post("/")
async def create_user(username: str):
    """创建用户"""
    return {"username": username}
```

#### 步骤 2: 注册路由

在 `app/routers/__init__.py` 中导入并注册到 `root_router`:

```python
# app/routers/__init__.py
from fastapi import APIRouter
from . import example, celery

# 创建根路由器
root_router = APIRouter()

# 注册各个模块的路由
root_router.include_router(example.router)
root_router.include_router(celery.router)
root_router.include_router(user.router)  # 新增 user 路由
```

### 3.2 create_router 函数

`create_router()` 函数位于 `app/routers/base.py`，作用：

- 自动设置 `prefix` 为 `/{sign}`
- 自动设置 `tags` 为 `[sign]`
- 保持 API 文档的结构清晰

```python
# app/routers/base.py
def create_router(sign):
    router = APIRouter()
    router.tags = [sign]
    router.prefix = f'/{sign}'
    return router
```

### 3.3 路由文件结构

每个路由文件应包含：

1. 必要的导入语句
2. 使用 `create_router()` 创建路由实例
3. 路由处理函数（带完整的文档字符串）
4. 相关的依赖和工具函数

---

## ⚡ 四、异步任务规范

### 4.1 任务定义位置

**所有异步任务必须定义在 `celery_tasks/` 目录中**

```
celery_tasks/
├── __init__.py        # Celery 实例初始化
├── worker.py          # Worker 启动入口
├── config.py          # Celery 配置
└── tasks/             # 任务定义 ⭐
    ├── __init__.py
    ├── example.py     # 示例任务
    └── logger_task.py # 日志测试任务
```

### 4.2 任务编写规范

```python
# celery_tasks/tasks/example.py
from celery_tasks import celery_app
from loguru import logger

@celery_app.task(bind=True)
def add_task(self, a, b):
    """
    简单的加法任务

    Args:
        a: 第一个数
        b: 第二个数

    Returns:
        两数之和
    """
    logger.info(f"执行任务：{a} + {b}")
    return a + b
```

### 4.3 任务调用

在 FastAPI 路由中调用异步任务：

```python
# app/routers/celery.py
from app.utils.celery_client import send_task

@router.post("/task/add")
async def run_add_task(a: int, b: int):
    """执行异步加法任务"""
    task_result = send_task(
        task_name="celery_tasks.tasks.example.add_task",
        args=[a, b],
        countdown=0  # 延迟执行秒数
    )
    return {
        "task_id": task_result.id,
        "status": task_result.status
    }
```

### 4.4 任务管理

- 任务名称应清晰表达功能
- 复杂任务应包含进度跟踪和错误处理
- 使用 `bind=True` 可以访问任务实例（用于更新状态、记录日志等）
- 参考 [`docs/CELERY_USAGE.md`](docs/CELERY_USAGE.md) 获取详细使用指南

---

## 📚 五、文档管理规范

### 5.1 文档分类

- **README.md**: 项目根目录，包含项目简介、快速开始、基础配置
- **docs/**: 所有其他技术文档

### 5.2 docs 目录内容

`docs/` 目录应包含：

- 功能模块详细说明（如 `CELERY_USAGE.md`）
- API 接口文档（如果超出 README 范围）
- 部署指南
- 开发规范
- 故障排查指南

### 5.3 文档更新原则

**核心原则：代码更改后，直接更新现有文档以保持同步**

#### 更新场景与操作指南：

1. **添加新功能模块**

   - ✅ 更新 `README.md` 的项目结构和 API 列表
   - ✅ 如功能复杂，在 `docs/` 中创建对应的技术文档（如 `CELERY_USAGE.md`）
   - ✅ 确保 Swagger 文档与代码一致
   - ❌ **不要**创建临时的"新增功能说明"或"变更日志"类文档

2. **修改现有接口**

   - ✅ **直接修改** `README.md` 中的 API 示例和说明
   - ✅ 如有必要，**直接修改** `docs/` 中的相关技术文档
   - ✅ 确保所有文档与实际代码保持一致
   - ❌ **不要**创建"重构说明"、"变更对比"等过渡性文档

3. **重构或优化**

   - ✅ **直接更新**现有文档中的架构说明和目录结构
   - ✅ 在现有文档中更新性能改进点
   - ✅ 确保文档准确反映当前实现
   - ❌ **不要**创建单独的重构记录文档（如 `REFACTOR_XXX.md`）

4. **配置变更**
   - ✅ **直接修改**现有文档中的配置说明章节
   - ✅ 提供最新的配置示例
   - ✅ 如有破坏性变更，在现有文档中添加迁移说明
   - ❌ **不要**创建配置变更记录文档

#### 文档维护要求：

- **单一来源原则**：每个技术点只在一个地方有详细说明，避免重复
- **实时更新**：代码提交前确保相关文档已更新完毕
- **准确性优先**：文档必须与实际代码行为完全一致
- **简洁实用**：只提供必要的技术说明，避免冗余

### 5.4 文档质量标准

- 使用清晰的标题层级
- 提供准确的代码示例
- 保持与代码实现同步
- 使用中文编写（与项目整体风格一致）
- **只维护必要的技术文档，避免创建临时性记录**

---

## 🔧 六、开发最佳实践

### 6.1 类型注解

- 所有函数参数和返回值都应使用类型注解
- 使用 `typing` 模块处理复杂类型
- Pydantic 模型优先于原始字典

```python
from typing import Any, Optional, List
from pydantic import BaseModel

def process_users(users: List[dict]) -> Optional[dict]:
    """处理用户列表"""
    if not users:
        return None
    return {"count": len(users)}
```

### 6.2 错误处理

使用装饰器统一处理异常：

```python
from app.utils.decorators import exception_handler

@router.get("/users/{user_id}")
@exception_handler
async def get_user(user_id: int):
    """获取用户信息"""
    if user_id not in database:
        raise ValueError(f"用户 {user_id} 不存在")
    return database[user_id]
```

### 6.3 日志记录

使用 Loguru 进行结构化日志：

```python
from loguru import logger

logger.info("服务启动成功")
logger.success("任务执行完成")
logger.warning("配置项缺失，使用默认值")
logger.error("数据库连接失败")
```

### 6.4 配置管理

- 使用 TOML 文件管理配置
- 不同环境使用不同的配置文件（`config.dev.toml`, `config.prod.toml`）
- 敏感信息通过环境变量覆盖

---

## 📋 七、检查清单

### 代码提交前检查

- [ ] 新模型是否放在 `app/models/` 目录？
- [ ] Request 模型是否继承自 `IBaseModel`？
- [ ] Response 模型是否继承自 `BaseResponse`？
- [ ] 路由是否分模块编写并使用 `create_router()`？
- [ ] 异步任务是否定义在 `celery_tasks/` 中？
- [ ] 是否更新了相关文档？
- [ ] 类型注解是否完整？
- [ ] 日志输出是否合理？

### 文档更新检查

- [ ] README.md 是否反映了最新的项目结构？
- [ ] docs/ 中的文档是否与代码实现一致？
- [ ] API 示例是否可以正常运行？
- [ ] 配置说明是否完整准确？
- [ ] **是否避免了创建不必要的临时文档（如重构说明、变更日志等）？**
- [ ] **所有修改是否直接更新到了现有文档中？**

---

## 🎯 八、快速参考

### 新建功能模块流程

1. **创建模型** → `app/models/my_feature.py`
2. **创建路由** → `app/routers/my_feature.py`（使用 `create_router("my_feature")`）
3. **注册路由** → 编辑 `app/routers/__init__.py`
4. **创建任务**（可选）→ `celery_tasks/tasks/my_feature.py`
5. **更新文档** → 更新 `README.md` 和/或创建 `docs/MY_FEATURE.md`

### 常用导入路径

```python
# 模型基类
from app.models.base import IBaseModel, BaseResponse

# 路由创建
from app.routers.base import create_router

# Celery 任务
from celery_tasks import celery_app

# 工具函数
from app.utils.celery_client import send_task
from app.utils.decorators import exception_handler
```

---

## 📞 九、支持与反馈

如有任何问题或建议，请：

1. 查阅 `README.md` 了解项目基本信息
2. 查看 `docs/` 目录下的详细文档
3. 参考代码注释和类型注解
4. 访问 FastAPI 官方文档：https://fastapi.tiangolo.com/zh/

---

**版本**: v0.1.0  
**最后更新**: 2026-03-04  
**维护者**: 项目团队
