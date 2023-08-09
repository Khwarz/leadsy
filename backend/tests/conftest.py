from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import Engine, RootTransaction, create_engine, event
from sqlalchemy.orm import Session, sessionmaker

from leadsy_api.core.config import get_settings
from leadsy_api.core.security import generate_hash
from leadsy_api.database.base import Base
from leadsy_api.database.session import get_db
from leadsy_api.main import app
from leadsy_api.models.users import User


@pytest.fixture()
def engine() -> Engine:
    return create_engine(get_settings().test_database_uri, echo=True)


@pytest.fixture()
def session_local(engine: Engine) -> sessionmaker[Session]:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session(
    engine: Engine, session_local: sessionmaker[Session]
) -> Generator[Session, None, None]:
    connection = engine.connect()
    transaction = connection.begin()
    session = session_local(bind=engine)
    nested = connection.begin_nested()

    @event.listens_for(session, "after_transaction_end")
    def after_transaction_end(session: Session, transaction: RootTransaction) -> None:
        nonlocal nested
        if not nested.is_active:
            nested = connection.begin_nested()

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture()
def client(session: Session) -> Generator[TestClient, None, None]:
    def override_get_db() -> Generator[Session, None, None]:
        yield session

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)
    del app.dependency_overrides[get_db]


@pytest.fixture()
def test_user() -> User:
    return User(
        full_name="John Doe",
        email="johndoe@example.com",
        hashed_password=generate_hash("password"),
    )
