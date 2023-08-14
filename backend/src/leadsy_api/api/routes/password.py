from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from leadsy_api.core.config import get_settings
from leadsy_api.core.mailing import send_email
from leadsy_api.core.security import generate_hash, generate_random_password_token
from leadsy_api.database.session import get_db
from leadsy_api.models.password_reset_tokens import PasswordResetToken
from leadsy_api.models.users import User
from leadsy_api.schemas.password import ForgotPasswordRequest, ResetPasswordRequest

router = APIRouter()


@router.post("/forgot-password")
async def forgot_password(
    forgot_password_request: ForgotPasswordRequest,
    db: Session = Depends(get_db),
) -> None:
    password_reset_token = db.scalars(
        select(PasswordResetToken).filter_by(email=forgot_password_request.email)
    ).first()

    if (
        password_reset_token is not None
        and password_reset_token.expires_at > datetime.now()
    ):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"You have to wait {get_settings().password_token_expires_minutes} before trying to reset your password",
        )

    if password_reset_token is not None:
        db.delete(password_reset_token)
        db.commit()

    token = generate_random_password_token()
    expires_at = datetime.now() + timedelta(
        minutes=get_settings().password_token_expires_minutes
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
            "reset_link": f"{get_settings().frontend_url}/password-reset/{password_reset_token.token}?email={password_reset_token.email}",
            "support_email": get_settings().mail_from_address,  # TODO: add support email
        },
    )


@router.post("/")
def reset_password(
    reset_password_request: ResetPasswordRequest, db: Session = Depends(get_db)
) -> None:
    password_reset_token = db.scalars(
        select(PasswordResetToken).filter_by(
            token=reset_password_request.token, email=reset_password_request.email
        )
    ).first()

    if password_reset_token is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Password reset token not found",
        )

    if password_reset_token.expires_at <= datetime.now():
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail=f"The reset token link has expired",
        )

    user = db.scalars(select(User).filter_by(email=password_reset_token.email)).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Your credentials are not valid",
        )

    user.hashed_password = generate_hash(reset_password_request.password)

    db.delete(password_reset_token)
    db.commit()
