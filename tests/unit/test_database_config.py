import pytest
from sqlalchemy.engine import Engine

from config.database import create_database_engine


@pytest.fixture
def mock_settings_sqlite(monkeypatch):
    """
    A fixture to mock SQLite database settings. It sets the database type to 'sqlite'
    and the database name to 'test_db', simulating an SQLite environment for testing.
    """

    class MockSettings:
        DB_TYPE = "sqlite"
        DB_NAME = "test_db"

    monkeypatch.setattr("config.app.get_settings", lambda: MockSettings())


@pytest.fixture
def mock_settings_psql(monkeypatch):
    """
    A fixture to mock PostgreSQL database settings. It configures the database type to 'psql'
    and sets other relevant settings such as database name, username, password, host, and port,
    simulating a PostgreSQL environment for testing.
    """

    class MockSettings:
        DB_TYPE = "psql"
        DB_NAME = "test_db"
        DB_USERNAME = "user"
        DB_PASSWORD = "pass"
        DB_HOST = "localhost"
        DB_PORT = 5432

    monkeypatch.setattr("config.app.get_settings", lambda: MockSettings())


@pytest.fixture
def mock_settings_mysql(monkeypatch):
    """
    A fixture to mock MySQL database settings. Similar to the PostgreSQL fixture, it sets
    the database type to 'mysql' along with the necessary database credentials and configurations,
    simulating a MySQL environment for testing.
    """

    class MockSettings:
        DB_TYPE = "mysql"
        DB_NAME = "test_db"
        DB_USERNAME = "user"
        DB_PASSWORD = "pass"
        DB_HOST = "localhost"
        DB_PORT = 3306

    monkeypatch.setattr("config.app.get_settings", lambda: MockSettings())


@pytest.fixture
def mock_settings_unsupported(monkeypatch):
    """
    A fixture to mock an unsupported database type. It sets the DB_TYPE to a string that
    is not recognized by the create_database_engine function, allowing testing of the error handling
    for unsupported database types.
    """

    class MockSettings:
        DB_TYPE = "unsupported_db_type"

    monkeypatch.setattr("config.app.get_settings", lambda: MockSettings())


def test_create_database_engine_sqlite(mock_settings_sqlite):
    """
    Given: SQLite database settings.
    When: Creating a database engine.
    Then: The engine should be an instance of SQLAlchemy Engine for SQLite.
    """
    engine = create_database_engine()
    assert isinstance(engine, Engine)


def test_create_database_engine_psql(mock_settings_psql):
    """
    Given: PostgreSQL database settings.
    When: Creating a database engine.
    Then: The engine should be an instance of SQLAlchemy Engine for PostgreSQL.
    """
    engine = create_database_engine()
    assert isinstance(engine, Engine)


def test_create_database_engine_mysql(mock_settings_mysql):
    """
    Given: MySQL database settings.
    When: Creating a database engine.
    Then: The engine should be an instance of SQLAlchemy Engine for MySQL.
    """
    engine = create_database_engine()
    assert isinstance(engine, Engine)
