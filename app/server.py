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
    validation_exception_handler
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 服务启动前执行
    init_logger()

    print_host = "127.0.0.1" if config.listen_host == "0.0.0.0" else config.listen_host
    docs_url = f"http://{print_host}:{config.listen_port}/docs"
    logger.success(f"服务启动成功, 查看文档: {docs_url}")
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
