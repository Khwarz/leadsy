from typing import Annotated

from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from leadsy_api.core.security import reusable_oauth_scheme
from leadsy_api.database.session import get_db
from leadsy_api.models.personal_access_tokens import PersonalAccessToken
from leadsy_api.models.users import User


async def get_current_user(
    token: Annotated[str, Depends(reusable_oauth_scheme)],
    db: Annotated[Session, Depends(get_db)],
) -> User:
    personal_access_token = db.scalars(
        select(PersonalAccessToken).filter_by(token=token)
    ).first()
    if personal_access_token is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    return personal_access_token.user
