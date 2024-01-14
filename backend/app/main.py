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


