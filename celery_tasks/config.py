import os
from app.utils import tools


# 加载配置文件
env = os.getenv("ENV", "dev")
env_config_file = os.path.join(os.path.dirname(
    os.path.dirname(__file__)), f"config.{env}.toml")
_env_config = tools.load_toml(env_config_file)


# Redis 配置
_redis_cfg: dict = _env_config.get("redis", {})
redis_host = _redis_cfg.get("host", "localhost")
redis_port = _redis_cfg.get("port", 6379)
redis_db = _redis_cfg.get("db", 0)
redis_password = _redis_cfg.get("password", "") or None


# Celery 配置
_celery_cfg: dict = _env_config.get("celery", {})
broker_url = _celery_cfg.get(
    "broker_url", f"redis://{redis_host}:{redis_port}/{redis_db}")
result_backend = _celery_cfg.get(
    "result_backend", f"redis://{redis_host}:{redis_port}/1")
task_serializer = _celery_cfg.get("task_serializer", "json")
result_serializer = _celery_cfg.get("result_serializer", "json")
accept_content = _celery_cfg.get("accept_content", ["json"])
timezone = _celery_cfg.get("timezone", "Asia/Shanghai")
enable_utc = _celery_cfg.get("enable_utc", True)


# Celery 配置字典
celery_config = {
    "broker_url": broker_url,
    "result_backend": result_backend,
    "task_serializer": task_serializer,
    "result_serializer": result_serializer,
    "accept_content": accept_content,
    "timezone": timezone,
    "enable_utc": enable_utc,
    "worker_hijack_root_logger": False,  # 不使用 Celery 的根日志，使用 Loguru
    "worker_log_level": _env_config.get("service", {}).get("log_level", "debug"),
}
