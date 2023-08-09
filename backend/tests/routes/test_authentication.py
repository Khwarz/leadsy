from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from leadsy_api.models.users import User


def test_it_should_generate_token(
    client: TestClient, session: Session, test_user: User
) -> None:
    session.add(test_user)
    session.commit()

    data = {"username": test_user.email, "password": "password"}
    response = client.post("/api/v1/oauth2/token", data=data)
    content = response.json()
    assert response.status_code == 200
    assert "accessToken" in content
    assert content["accessToken"] is not None


def test_it_should_not_work_with_invalid_credentials(
    client: TestClient, session: Session, test_user: User
) -> None:
    session.add(test_user)
    session.commit()

    data = {"username": test_user.email, "password": "wrong-password"}
    response = client.post("/api/v1/oauth2/token", data=data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_it_should_not_work_with_unknown_user(
    client: TestClient,
) -> None:
    data = {"username": "someone@example.com", "password": "wrong-password"}
    response = client.post("/api/v1/oauth2/token", data=data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
