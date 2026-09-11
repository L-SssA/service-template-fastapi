import importlib
from pathlib import Path

module_path = Path(__file__).parent

def load_models():
    """加载所有 sqlalchemy 模型"""
    package = f"{__name__}." if __name__ != "__main__" else ""
    for module in module_path.iterdir():
        # 过滤出有models.py的模块目录
        if not module.is_dir() or module.name.startswith("__") or not (module / "models.py").exists():
            continue
        # 导入模块
        print(package + f"{module.name}.models")
        importlib.import_module(package + f"{module.name}.models")
