from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from leadsy_api.api.routes import router as api_router
from leadsy_api.core.config import get_settings


def get_application() -> FastAPI:
    app = FastAPI(title=get_settings().app_name, version="0.0.1")
    app.include_router(router=api_router, prefix="/api")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )
    return app


app = get_application()
