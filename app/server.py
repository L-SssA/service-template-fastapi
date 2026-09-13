import app.config as config

from loguru import logger
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


from .utils import sys_utils
from .utils.celery_client import celery_client
from .utils.logger import init_logger
from .routers import register_routers
from .exceptions import register_exception_handlers
from .middlewares import register_middleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 服务启动前执行
    init_logger()

    docs_url = f"http://{config.print_host}:{config.listen_port}/docs"
    logger.success(f"服务启动成功，启动环境 {config.env}，查看文档：{docs_url}")
    yield
    # 服务关闭前执行
    logger.success("服务关闭")

app: FastAPI = FastAPI(
    title=config.project_name,
    description=config.project_description,
    version=config.project_version,
    debug=config.log_level == "debug",
    lifespan=lifespan
)

# 注册路由
register_routers(app)

# 全局错误拦截器
register_exception_handlers(app)

# 中间件
register_middleware(app)

# 挂载静态文件夹
public_path = sys_utils.root_dir("public")
app.mount("/", StaticFiles(directory=public_path, html=True), name="public")
