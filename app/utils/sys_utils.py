
from pathlib import Path

from loguru import logger


def safe_create_dir(path: str | Path) -> Path:
    """安全创建目录并返回标准化的 pathlib.Path 对象。"""
    directory = Path(path)
    try:
        if not directory.exists():
            directory.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        logger.error(f"safe_create_dir error: {e}")
    return directory


def _root_dir() -> Path:
    """获取项目根目录。"""
    return Path(__file__).resolve().parents[2]


def root_dir(dir_path: str | Path = "") -> Path:
    """基于项目根目录返回指定目录路径，若目录不存在则创建。"""
    directory = _root_dir() / Path(dir_path)
    if not directory.exists():
        safe_create_dir(directory)
    return directory

def app_dir() -> Path:
    return root_dir() / "app"
