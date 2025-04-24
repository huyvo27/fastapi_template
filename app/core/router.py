import importlib
import pkgutil
from fastapi import APIRouter
from pathlib import Path

API_PATH = Path(__file__).parent.parent / "api"
API_PATH_V1 = API_PATH / "v1"

def auto_include_routers(package: str, path: Path):
        router = APIRouter()
        for _, module_name, is_pkg in pkgutil.iter_modules([str(path)]):
            if not is_pkg:
                module_path = f"{package}.{module_name}"
                module = importlib.import_module(module_path)
                if hasattr(module, "router"):
                    router.include_router(getattr(module, "router"), prefix= "/" + module_name, tags=[module_name])
        return router

router = auto_include_routers("app.api", API_PATH)

v1_router = auto_include_routers("app.api.v1", API_PATH_V1)

router.include_router(v1_router, prefix="/v1")