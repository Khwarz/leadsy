from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from leadsy_api.models.password_reset_tokens import PasswordResetToken


def test_it_should_register_password_reset_links(
    client: TestClient, session: Session
) -> None:
    response = client.post(
        "/api/v1/password/forgot-password", json={"email": "johndoe@gmail.com"}
    )
    password_reset_token = session.scalars(
        select(PasswordResetToken).filter_by(email="johndoe@gmail.com")
    ).first()
    assert response.status_code == 200
    assert password_reset_token is not None
