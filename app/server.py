from loguru import logger
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from app.config import config
from app.utils import sys_utils
from app.routers import root_router
from app.utils.logger import init_logger
from app.utils.server import (
    validation_exception_handler,
    http_exception_handler
)


def _check_celery_status():
    """
    检查 Celery 连接状态并输出日志

    Returns:
        dict: 检查结果
    """
    from app.utils.celery_client import check_celery_connection

    result = check_celery_connection(timeout=3)

    if result["connected"]:
        if result["workers_count"] > 0:
            logger.success(f"检测到 {result['workers_count']} 个活跃的 Celery Worker")
        else:
            logger.warning("未检测到活跃的 Celery Worker，异步任务可能无法执行")
            logger.warning(f"提示：{result['error']}")
    else:
        logger.warning(f"Celery 连接失败：{result['error']}")
        logger.warning("异步任务功能将不可用，请确保 Redis 和 Celery Worker 已启动")

    return result


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 服务启动前执行
    init_logger()

    # Celery 连接性检查
    _check_celery_status()

    print_host = "127.0.0.1" if config.listen_host == "0.0.0.0" else config.listen_host
    docs_url = f"http://{print_host}:{config.listen_port}/docs"
    logger.success(f"服务启动成功，查看文档：{docs_url}")
    yield
    # 服务关闭前执行
    logger.success("服务关闭")

app: FastAPI = FastAPI(
    title=config.project_name,
    description=config.project_description,
    version=config.project_version,
    debug=False,
    lifespan=lifespan
)

# 注册路由
app.include_router(root_router)

# 全局错误拦截器
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, http_exception_handler)

# cors 设置
cors_allow_origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载路由
public_path = sys_utils.root_dir("public")
app.mount("/", StaticFiles(directory=public_path, html=True), name="public")
