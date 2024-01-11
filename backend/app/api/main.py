from backend.app.core.server import configure_server


app = configure_server()


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    app