import os
import argparse

from app.utils import sys_utils, tools

# 命令行参数解析
parser = argparse.ArgumentParser(description="FastAPI 服务")
parser.add_argument(
    "--env",
    type=str,
    default="dev",
    help="环境标识（任意标识，与环境配置文件对应）",
)

args, _unknown_args = parser.parse_known_args()
os.environ["ENV"] = args.env

# 配置文件加载
project_config_file = os.path.join(sys_utils.root_dir(), "pyproject.toml")

# pyproject.toml 相关配置
project_config = tools.load_toml(project_config_file)
_project_cfg_ = project_config.get("project", {})
project_name = _project_cfg_.get("name", "")
project_description = _project_cfg_.get("description", "")
project_version = _project_cfg_.get("version", "")

# config.{env}.toml 与环境相关的配置
env = os.getenv("ENV", "dev")
env_config_file = os.path.join(sys_utils.root_dir(), f"config.{env}.toml")
_env_config = tools.load_toml(env_config_file)


# service 相关配置
_service_cfg: dict = _env_config.get("service", {})
listen_host = _service_cfg.get("listen_host", "0.0.0.0")
listen_port = _service_cfg.get("listen_port", 8800)
log_level = _service_cfg.get("log_level", "debug")
reload_debug = _service_cfg.get("reload_debug", False)

# sql 相关配置
_sql_cfg: dict = _env_config.get("sql", {})
sql_host = _sql_cfg.get("host", "localhost")
sql_port = _sql_cfg.get("port", 5432)
sql_username = _sql_cfg.get("username", "postgres")
sql_password = _sql_cfg.get("password", "123456")
sql_dbname = _sql_cfg.get("dbname", "mypostgres")
sql_url = f"postgresql+asyncpg://{sql_username}:{sql_password}@{sql_host}:{sql_port}/{sql_dbname}"
