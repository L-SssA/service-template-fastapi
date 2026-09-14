from pydantic_settings import BaseSettings, SettingsConfigDict
import os
from app.utils import tools


class EnvSettings(BaseSettings):
    """环境标识"""
    ENV: str = "dev"

    """MAIL 配置"""
    MAIL_USERNAME: str = ""
    MAIL_PASSWORD: str = ""
    MAIL_FROM: str = ""

    model_config = SettingsConfigDict(
        env_file='.env', extra='ignore', env_file_encoding='utf-8')


env_settings = EnvSettings()

# 加载配置文件
env = env_settings.ENV
env_config_file = os.path.join(os.path.dirname(
    os.path.dirname(__file__)), f"config.{env}.toml")
_env_config = tools.load_toml(env_config_file)


# Redis 配置
_redis_cfg: dict = _env_config.get("redis", {})
redis_host = _redis_cfg.get("host", "localhost")
redis_port = _redis_cfg.get("port", 6379)
redis_db = _redis_cfg.get("db", 0)
redis_db_1 = _redis_cfg.get("db_1", 1)
redis_url = f"redis://{redis_host}:{redis_port}/{redis_db}"
redis_url_1 = f"redis://{redis_host}:{redis_port}/{redis_db_1}"
redis_password = _redis_cfg.get("password", "") or None


# Celery 配置
_celery_cfg: dict = _env_config.get("celery", {})
broker_url = _celery_cfg.get("broker_url", redis_url)
result_backend = _celery_cfg.get("result_backend", redis_url_1)
task_serializer = _celery_cfg.get("task_serializer", "json")
result_serializer = _celery_cfg.get("result_serializer", "json")
accept_content = _celery_cfg.get("accept_content", ["json"])
timezone = _celery_cfg.get("timezone", "Asia/Shanghai")
enable_utc = _celery_cfg.get("enable_utc", True)
log_level = _celery_cfg.get("log_level", "info")


# mail 相关配置
_mail_cfg: dict = _env_config.get("mail", {})
mail_username = _mail_cfg.get("username", "") or env_settings.MAIL_USERNAME
mail_password = _mail_cfg.get("password", "") or env_settings.MAIL_PASSWORD
mail_server = _mail_cfg.get("mail_server", "")
mail_port = _mail_cfg.get("mail_port", 465)
mail_from = _mail_cfg.get("mail_from", "") or env_settings.MAIL_FROM
mail_from_name = _mail_cfg.get("mail_from_name", "")
