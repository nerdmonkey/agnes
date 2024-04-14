from sqlalchemy.orm import declarative_base

Base = declarative_base()


def test_base_creation():
    """
    Test to ensure that the SQLAlchemy Base class is successfully created.

    This test checks if the Base class, which is generated using SQLAlchemy's
    declarative_base function, is instantiated correctly. The Base class is
    essential for defining SQLAlchemy ORM models. A successful creation of the
    Base class is indicated if it is not None after instantiation.
    """
    assert Base is not None
