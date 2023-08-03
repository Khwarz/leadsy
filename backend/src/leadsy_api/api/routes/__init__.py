from fastapi import APIRouter

from leadsy_api.api.routes.authentication import router as auth_router

router = APIRouter()

router.include_router(auth_router, prefix="/oauth2", tags=["authentication"])
