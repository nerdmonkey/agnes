import os
from unittest.mock import patch

from config.app import Settings, get_settings


def test_settings_loads_env_vars():
    """
    Test that the Settings class correctly loads configuration from environment variables.

    This test sets environment variables and then creates a Settings instance to
    verify that the environment variables are correctly loaded and assigned.
    """
    os.environ["ALLOWED_ORIGINS"] = "http://example.com"
    os.environ["APP_ENVIRONMENT"] = "test"
    os.environ["DB_TYPE"] = "sqlite"
    os.environ["DB_HOST"] = "localhost"
    os.environ["DB_NAME"] = "testdb"
    os.environ["DB_USERNAME"] = "user"
    os.environ["DB_PASSWORD"] = "password"

    settings = Settings()

    assert settings.ALLOWED_ORIGINS == "http://example.com"
    assert settings.APP_ENVIRONMENT == "test"
    assert settings.DB_TYPE == "sqlite"
    assert settings.DB_HOST == "localhost"
    assert settings.DB_NAME == "testdb"
    assert settings.DB_USERNAME == "user"
    assert settings.DB_PASSWORD == "password"


def test_get_settings_cached():
    """
    Test that the get_settings function is using cache for returning the Settings.

    This test verifies that when get_settings is called multiple times, it returns
    the same instance of Settings, indicating that the function's result is being cached.
    """
    with patch("config.app.Settings", return_value=Settings()):
        first_call = get_settings()
        second_call = get_settings()

    assert first_call is second_call
