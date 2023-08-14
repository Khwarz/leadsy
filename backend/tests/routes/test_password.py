from datetime import datetime, timedelta

from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from leadsy_api.core.config import get_settings
from leadsy_api.core.mailing import mailer
from leadsy_api.core.security import check_password, generate_random_password_token
from leadsy_api.models.password_reset_tokens import PasswordResetToken
from leadsy_api.models.users import User


def test_it_should_register_password_reset_links(
    client: TestClient, session: Session
) -> None:
    mailer.config.SUPPRESS_SEND = 1
    with mailer.record_messages() as outbox:
        response = client.post(
            "/api/v1/password-reset/forgot-password",
            json={"email": "johndoe@gmail.com"},
        )
        password_reset_token = session.scalars(
            select(PasswordResetToken).filter_by(email="johndoe@gmail.com")
        ).first()
        assert response.status_code == 200
        assert password_reset_token is not None
        assert outbox[0]["to"] == "johndoe@gmail.com"


def test_it_should_update_user_password(
    client: TestClient, session: Session, test_user: User
) -> None:
    token = generate_random_password_token()
    session.add(
        PasswordResetToken(
            email=test_user.email,
            token=token,
            expires_at=datetime.now()
            + timedelta(minutes=get_settings().password_token_expires_minutes),
        )
    )
    session.commit()
    response = client.post(
        "/api/v1/password-reset",
        json={
            "email": test_user.email,
            "token": token,
            "password": "new-password",
            "passwordConfirmation": "new-password",
        },
    )
    session.refresh(test_user)
    assert response.status_code == 200
    assert check_password(plain_text="new-password", password=test_user.hashed_password)
    assert session.query(PasswordResetToken).count() == 0
