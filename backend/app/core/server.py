from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware


def configure_server():
    """Creates and configures fastapi application."""
    app = FastAPI()

    ALLOWED_ORIGINS = [
        "*",
        "http://127.0.0.1:8000",
        "http://0.0.0.0:8000",
        "http://localhost:8000",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app
