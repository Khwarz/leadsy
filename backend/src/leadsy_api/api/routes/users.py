from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from leadsy_api.database.session import get_db
from leadsy_api.models.users import User
from leadsy_api.schemas.users import UserCreate

router = APIRouter()


@router.post("/")
def create_user(
    db: Annotated[Session, Depends(get_db)], user_create: UserCreate
) -> None:
    user = User(**dict(user_create), hashed_password=user_create.password + "nothashed")
    db.add(user)
    db.commit()
