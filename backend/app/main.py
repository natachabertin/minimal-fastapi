from backend.app.api.routes.routes_definitions import expose_routes
from backend.app.core.server import configure_server


app = configure_server()


app = expose_routes(app)


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    app