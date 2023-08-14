from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from leadsy_api.core.config import get_settings
from leadsy_api.core.mailing import send_email
from leadsy_api.core.security import generate_random_password_token
from leadsy_api.database.session import get_db
from leadsy_api.models.password_reset_tokens import PasswordResetToken
from leadsy_api.schemas.password import ForgotPasswordRequest

router = APIRouter()


@router.get("/forgot-password")
async def forgot_password(
    forgot_password_request: ForgotPasswordRequest,
    db: Session = Depends(get_db),
) -> None:
    password_reset_token = db.scalars(
        select(PasswordResetToken).filter_by(email=forgot_password_request.email)
    ).first()

    if (
        password_reset_token is not None
        and password_reset_token.expires_at < datetime.now()
    ):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many password reset tokens links requested",
        )

    if password_reset_token is not None:
        db.delete(password_reset_token)
        db.commit()

    token = generate_random_password_token()
    expires_at = datetime.now() + timedelta(
        seconds=get_settings().password_token_expires_seconds
    )
    password_reset_token = PasswordResetToken(
        email=forgot_password_request.email, token=token, expires_at=expires_at
    )
    db.add(password_reset_token)
    db.commit()
    await send_email(
        recipient=forgot_password_request.email,
        subject="Password Reset URL for your account",
        template_name="forgot_password.html",
        data={
            "reset_link": router.url_path_for(
                "reset_password", token=password_reset_token.token
            ),
            "support_email": "",  # TODO: add support email
        },
    )
