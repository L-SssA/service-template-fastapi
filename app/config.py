import os
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.utils import sys_utils, tools

class EnvSettings(BaseSettings):
    """环境标识"""
    ENV: str = "dev"

    """PGSQL 配置"""
    PGSQL_USERNAME: str = ""
    PGSQL_PASSWORD: str = ""

    """JWT 配置"""
    JWT_SECRET: str = ""

    """MAIL 配置"""
    MAIL_USERNAME: str = ""
    MAIL_PASSWORD: str = ""
    MAIL_FROM_EMAIL: str = ""

    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8')


env_settings = EnvSettings()

# 配置文件加载
project_config_file = os.path.join(sys_utils.root_dir(), "pyproject.toml")

# pyproject.toml 相关配置
project_config = tools.load_toml(project_config_file)
_project_cfg_: dict = project_config.get("project", {})
project_name = _project_cfg_.get("name", "")
project_description = _project_cfg_.get("description", "")
project_version = _project_cfg_.get("version", "")

# config.{env}.toml 与环境相关的配置
env = env_settings.ENV
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
sql_username = _sql_cfg.get("username", "") or env_settings.PGSQL_USERNAME
sql_password = _sql_cfg.get("password", "") or env_settings.PGSQL_PASSWORD
sql_dbname = _sql_cfg.get("dbname", "mypostgres")
sql_url = f"postgresql+asyncpg://{sql_username}:{sql_password}@{sql_host}:{sql_port}/{sql_dbname}"

# Redis 配置
_redis_cfg: dict = _env_config.get("redis", {})
redis_host = _redis_cfg.get("host", "localhost")
redis_port = _redis_cfg.get("port", 6379)
redis_db = _redis_cfg.get("db", 0)
redis_jti_expiry_seconds = _redis_cfg.get("jti_expiry_seconds", 3600)

# 认证相关配置
_auth_cfg: dict = _env_config.get("auth", {})
jwt_secret_key = _auth_cfg.get("jwt_secret", "") or env_settings.JWT_SECRET
jwt_algorithm = _auth_cfg.get("jwt_algorithm", "HS256")
jwt_expiry_seconds = _auth_cfg.get("jwt_expiry_seconds", 3600)
jwt_refresh_expiry_seconds = _auth_cfg.get("jwt_refresh_expiry_seconds", 86400)

# mail 相关配置
_mail_cfg: dict = _env_config.get("mail", {})
mail_username = _mail_cfg.get("username", "") or env_settings.MAIL_USERNAME
mail_password = _mail_cfg.get("password", "") or env_settings.MAIL_PASSWORD
mail_server = _mail_cfg.get("mail_server", "")
mail_port = _mail_cfg.get("mail_port", 465)
mail_from_email = _mail_cfg.get(
    "from_email", "") or env_settings.MAIL_FROM_EMAIL
mail_from_name = _mail_cfg.get("from_name", "")
