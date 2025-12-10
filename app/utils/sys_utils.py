
import os
from loguru import logger

def safe_create_dir(path):
    """安全创建目录"""
    try:
        if not os.path.exists(path):
            os.makedirs(path)
    except Exception as e:
        logger.error(f"safe_create_dir error: {e}")


def _root_dir():
    """获取项目根目录"""
    return os.path.realpath(os.path.join(os.path.realpath(__file__), "../../../"))


def root_dir(dir_path: str = ""):
    d = os.path.join(_root_dir(), dir_path)
    if not os.path.exists(d):
        safe_create_dir(d)
    return d
