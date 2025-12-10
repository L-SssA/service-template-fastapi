import os
from app.utils import sys_utils, tools


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
