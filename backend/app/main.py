from functools import lru_cache

from fastapi import Depends
from typing_extensions import Annotated

from app.api.routes.routes_definitions import expose_routes
from app.core import config
from app.core.config import Settings
from app.core.server import configure_server

@lru_cache()
def get_settings():
    return Settings()


app = configure_server()
settings = get_settings()


app = expose_routes(app)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/set")
async def info(settings: Annotated[config.Settings, Depends(get_settings)]):
    print(settings)
    return {
        "app_name": settings.app_name,
        "admin_email": settings.admin_email,
        "items_per_user": settings.items_per_user,
    }
