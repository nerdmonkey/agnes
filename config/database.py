from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session as SQLAlchemySession
from sqlalchemy.orm import sessionmaker

from config.app import get_settings


def create_database_engine() -> Engine:
    settings = get_settings()
    database_type = settings.DB_TYPE
    database = settings.DB_NAME

    # Mapping for different database types to their URL formats
    url_formats = {
        "sqlite": f"sqlite:///./database/{database}.db",
        "psql": "postgresql+pg8000://{username}:{password}@{host}:{port}/{database}",
        "mysql": "mysql+pymysql://{username}:{password}@{host}:{port}/{database}",
        "mssql": "mssql+pyodbc://{username}:{password}@{host}:{port}/{database}?driver={driver}",
    }

    if database_type in url_formats:
        database_url = url_formats[database_type]
        if database_type != "sqlite":
            database_url = database_url.format(
                username=settings.DB_USERNAME,
                password=settings.DB_PASSWORD,
                host=settings.DB_HOST,
                port=settings.DB_PORT,
                database=database,
                driver=settings.DB_DRIVER,
            )
        return create_engine(
            database_url,
            connect_args={"check_same_thread": False}
            if database_type == "sqlite"
            else {},
        )

    raise ValueError(f"Unsupported database type: {database_type}")


engine = create_database_engine()
Session = sessionmaker(bind=engine)


def get_session() -> SQLAlchemySession:
    return Session()
