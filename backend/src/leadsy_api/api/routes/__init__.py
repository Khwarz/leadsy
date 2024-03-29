from fastapi import APIRouter

from leadsy_api.api.routes.authentication import router as auth_router
from leadsy_api.api.routes.password import router as password_router
from leadsy_api.api.routes.users import router as users_router

router = APIRouter()

router.include_router(auth_router, prefix="/oauth2", tags=["authentication"])
router.include_router(users_router, prefix="/users", tags=["users"])
router.include_router(
    password_router, prefix="/password-reset", tags=["password-reset"]
)
