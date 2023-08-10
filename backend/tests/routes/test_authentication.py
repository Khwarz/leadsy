from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from leadsy_api.models.access_tokens import PersonalAccessToken
from leadsy_api.models.users import User


def test_it_should_generate_token(
    client: TestClient, session: Session, test_user: User
) -> None:
    data = {"username": test_user.email, "password": "password"}
    response = client.post("/api/v1/oauth2/token", data=data)
    content = response.json()
    personal_access_token = session.scalars(
        select(PersonalAccessToken).filter_by(token=content["accessToken"])
    ).first()
    assert response.status_code == 200
    assert "accessToken" in content
    assert content["accessToken"] is not None
    assert personal_access_token is not None
    assert personal_access_token.token == content["accessToken"]


def test_it_should_not_work_with_invalid_credentials(
    client: TestClient, test_user: User
) -> None:
    data = {"username": test_user.email, "password": "wrong-password"}
    response = client.post("/api/v1/oauth2/token", data=data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_it_should_not_work_with_unknown_user(
    client: TestClient,
) -> None:
    data = {"username": "someone@example.com", "password": "wrong-password"}
    response = client.post("/api/v1/oauth2/token", data=data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_it_should_revoke_access_token(
    client: TestClient,
    test_user_access_token: str,
    test_auth_headers: dict[str, str],
    session: Session,
) -> None:
    response = client.post(
        "/api/v1/oauth2/revoke",
        headers=test_auth_headers,
        json={"token": test_user_access_token},
    )
    personal_access_token = session.scalars(
        select(PersonalAccessToken).filter_by(token=test_user_access_token)
    ).first()
    assert response.status_code == status.HTTP_200_OK
    assert personal_access_token is None
