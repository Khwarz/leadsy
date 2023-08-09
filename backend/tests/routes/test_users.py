from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from leadsy_api.models.users import User


def test_it_should_create_users(client: TestClient, session: Session) -> None:
    data = {
        "fullName": "John Doe",
        "email": "johndoe@example.com",
        "password": "password",
    }
    response = client.post("/api/v1/users", json=data)
    assert response.status_code == status.HTTP_200_OK
    user = next(session.execute(select(User)).scalars(), None)
    assert user is not None
    assert user.full_name == "John Doe"
    assert user.email == "johndoe@example.com"
    assert user.email_verified_at is None


def test_it_should_not_create_users_when_name_is_empty(
    client: TestClient, session: Session
) -> None:
    data = {
        "fullName": "",
        "email": "johndoe@example.com",
        "password": "password",
    }
    response = client.post("/api/v1/users", json=data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    user = next(session.execute(select(User)).scalars(), None)
    assert user is None


def test_it_should_not_create_users_when_email_is_incorrect(
    client: TestClient, session: Session
) -> None:
    data = {
        "fullName": "John Doe",
        "email": "wrong-email",
        "password": "password",
    }
    response = client.post("/api/v1/users", json=data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    user = next(session.execute(select(User)).scalars(), None)
    assert user is None


def test_it_should_not_create_users_when_password_is_short(
    client: TestClient, session: Session
) -> None:
    data = {
        "fullName": "John Doe",
        "email": "johndoe@example.com",
        "password": "short",
    }
    response = client.post("/api/v1/users", json=data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    user = next(session.execute(select(User)).scalars(), None)
    assert user is None


def test_it_should_not_create_users_when_email_already_exists(
    client: TestClient, session: Session, test_user: User
) -> None:
    session.add(test_user)
    session.commit()
    data = {
        "fullName": "John Doe",
        "email": test_user.email,
        "password": "password",
    }
    response = client.post("/api/v1/users", json=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
