from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware


def configure_server(settings):
    """Creates and configures fastapi application."""
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=settings.allowed_methods,
        allow_headers=settings.allowed_headers,
    )

    return app
