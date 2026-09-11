import importlib
from pathlib import Path


def load_tasks():
    module_path = Path(__file__).parent
    package = f"{__name__}." if __name__ != "__main__" else ""

    for module in module_path.iterdir():
        if module.name.startswith("__"):
            continue
        importlib.import_module(package + f"{module.stem}")
