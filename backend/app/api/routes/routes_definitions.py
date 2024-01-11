from backend.app.api.routes.samples import router as sample_router


def expose_routes(app):
    app.include_router(sample_router, prefix="/sample")

    return app
