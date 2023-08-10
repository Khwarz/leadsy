from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from leadsy_api.api.dependencies import get_current_user
from leadsy_api.core.security import check_password, create_access_token
from leadsy_api.database.session import get_db
from leadsy_api.models.personal_access_tokens import PersonalAccessToken
from leadsy_api.models.users import User
from leadsy_api.schemas.token import AccessTokenResponse

router = APIRouter()


@router.post("/token")
async def generate_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)],
) -> AccessTokenResponse:
    user = db.scalars(select(User).filter_by(email=form_data.username)).first()
    if (not user) or (not check_password(form_data.password, user.hashed_password)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Your credentials does not match our records",
        )
    access_token = create_access_token(user.email)
    db.add(PersonalAccessToken(user_id=user.id, token=access_token))
    db.commit()
    return AccessTokenResponse(token_type="Bearer", access_token=access_token)


@router.post("/revoke")
async def revoke_access_token(
    _: Annotated[User, Depends(get_current_user)],
    token: str,
    db: Annotated[Session, Depends(get_db)],
) -> None:
    personal_access_token = db.scalars(
        select(PersonalAccessToken).filter_by(token=token)
    ).first()
    db.delete(personal_access_token)
    db.commit()
