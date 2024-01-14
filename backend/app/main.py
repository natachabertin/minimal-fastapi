from functools import lru_cache

from app.api.routes.routes_definitions import expose_routes
from app.core.config import Settings
from app.core.server import configure_server

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()
app = configure_server(settings)


app = expose_routes(app)


@app.get("/")
async def root():
    return {"message": "Hello World"}


