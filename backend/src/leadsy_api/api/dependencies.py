from datetime import datetime
from typing import Annotated

from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from leadsy_api.core.security import reusable_oauth_scheme
from leadsy_api.database.session import get_db
from leadsy_api.models.access_tokens import PersonalAccessToken
from leadsy_api.models.users import User


async def get_current_user(
    token: Annotated[str, Depends(reusable_oauth_scheme)],
    db: Annotated[Session, Depends(get_db)],
) -> User:
    credentials_exception = HTTPException(status_code=401, detail="Invalid token")
    personal_access_token = db.scalars(
        select(PersonalAccessToken).filter_by(token=token)
    ).first()
    if personal_access_token is None or personal_access_token.user is None:
        raise credentials_exception

    if (
        personal_access_token.expires_at is not None
        and personal_access_token.expires_at < datetime.now()
    ):
        raise credentials_exception
    return personal_access_token.user
