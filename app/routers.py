from importlib import import_module
from pathlib import Path
from fastapi import APIRouter

root_router = APIRouter()

modules_dir = Path(__file__).resolve().parent / "modules"

for module_dir in modules_dir.iterdir():
    if not module_dir.is_dir() or module_dir.name.startswith("__"):
        continue

    routes_file = module_dir / "routes.py"
    if not routes_file.exists():
        continue

    module_name = f"app.modules.{module_dir.name}.routes"
    route_module = import_module(module_name)
    router = getattr(route_module, "router", None)
    if router is not None:
        root_router.include_router(router)
