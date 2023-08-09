from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from leadsy_api.core.security import generate_hash
from leadsy_api.database.session import get_db
from leadsy_api.models.users import User
from leadsy_api.schemas.users import UserCreate

router = APIRouter()


@router.post("/")
def create_user(
    db: Annotated[Session, Depends(get_db)], user_create: UserCreate
) -> None:
    user = db.execute(select(User).where(User.email == user_create.email)).first()
    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The email is already registered",
        )
    new_user = User(
        full_name=user_create.full_name,
        email=user_create.email,
        hashed_password=generate_hash(user_create.password),
    )
    db.add(new_user)
    db.commit()
