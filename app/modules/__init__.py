import importlib
from pathlib import Path

module_path = Path(__file__).parent

def load_models():
    for module in module_path.iterdir():
        # 过滤出有models.py的模块目录
        if not module.is_dir() or module.name.startswith("__") or not (module / "models.py").exists():
            continue
        # 导入模块
        importlib.import_module(f"{__name__}.{module.name}.models")
