import logging
from functools import lru_cache
from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseSettings, validator

load_dotenv(dotenv_path=".env")

# Configure the logger
log = logging.getLogger("uvicorn")


class Settings(BaseSettings):
    """
    Configuration class for application settings.

    Settings are loaded from environment variables, which are read from an environment
    file. The default environment file is '.env', but this can be overridden based on
    the 'APP_ENVIRONMENT' variable to support different configurations for different
    environments (like local development or production).

    Attributes:
        ALLOWED_ORIGINS (str): Comma-separated list of allowed origins for CORS.
        APP_ENVIRONMENT (str): The current environment of the app (e.g., local, production).
        DB_TYPE (str): Type of the database (e.g., sqlite, postgres).
        DB_DRIVER (str): Driver of the database (e.g., ODBC+Driver+17+for+SQL+Server).
        DB_HOST (str): Host address of the database.
        DB_PORT (Optional[int]): Port number of the database. Can be None.
        DB_NAME (str): Name of the database.
        DB_USERNAME (str): Username for the database.
        DB_PASSWORD (str): Password for the database.
    """

    ALLOWED_ORIGINS: str
    APP_ENVIRONMENT: str
    APP_DEBUG: bool
    DB_TYPE: str
    DB_DRIVER: str
    DB_HOST: str
    DB_PORT: Optional[int] = None
    DB_NAME: str
    DB_USERNAME: str
    DB_PASSWORD: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @validator("DB_PORT", pre=True, always=True)
    def default_db_port(cls, v):
        try:
            return int(v)
        except (TypeError, ValueError):
            return None


@lru_cache()
def get_settings() -> Settings:
    """
    Retrieve and cache the application settings.

    This function reads the 'APP_ENVIRONMENT' environment variable to determine the
    appropriate environment file to use ('.env' or '.env_testing'). The settings are then
    loaded from the specified environment file and cached for future use.

    Returns:
        Settings: The loaded and cached application settings.
    """

    log.info("Loading config settings from the environment...")

    return Settings()
