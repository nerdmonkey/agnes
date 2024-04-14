import os

import pytest
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

from app.models.base import Base
from app.models.user import User
from config.database import get_session
from public.main import app

load_dotenv(dotenv_path=".env_testing")

get_db = get_session()


def construct_database_url():
    db_type = os.environ.get("DB_TYPE", "sqlite")
    db_name = "spartan.db"
    if db_type == "sqlite":
        return f"sqlite:///./database/{db_name}"
    else:
        db_host = os.getenv("DB_HOST", "localhost")
        db_port = os.getenv("DB_PORT", "5432")
        db_username = os.getenv("DB_USERNAME", "user")
        db_password = os.getenv("DB_PASSWORD", "password")

        if db_type == "psql":
            return f"postgresql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"

        elif db_type == "mysql":
            return f"mysql+pymysql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"
        else:
            raise ValueError(f"Unsupported database type: {db_type}")

    raise ValueError(f"Unsupported database type: {db_type}")


@pytest.fixture(scope="module")
def test_db_session():
    TEST_DATABASE_URL = construct_database_url()

    engine = create_engine(TEST_DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    db = TestingSessionLocal()

    yield db

    db.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="module")
def test_data(test_db_session):
    users = [
        User(
            username=f"testuser{i}",
            email=f"testuser{i}@example.com",
            password="password123",
        )
        for i in range(1, 6)
    ]

    for user in users:
        test_db_session.add(user)
    test_db_session.commit()

    yield users

    for user in users:
        test_db_session.delete(user)
    test_db_session.commit()


@pytest.fixture(scope="function")
def client(test_db_session):
    app.dependency_overrides[get_db] = lambda: test_db_session

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
