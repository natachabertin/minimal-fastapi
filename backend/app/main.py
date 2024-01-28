from app.api.routes.routes_definitions import expose_routes
from app.core.config import settings
from app.core.server import configure_server


app = configure_server(settings)

app = expose_routes(app)


@app.get("/")
async def root():
    return {"message": "Hello World"}


