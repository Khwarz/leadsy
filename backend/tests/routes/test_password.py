from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from leadsy_api.core.mailing import mailer
from leadsy_api.models.password_reset_tokens import PasswordResetToken


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
