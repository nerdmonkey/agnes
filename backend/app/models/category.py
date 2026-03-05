from sqlalchemy import Column, Integer, String, Text, func, DateTime
from sqlalchemy.orm import relationship

from .base import Base


class Category(Base):
    """
    Database model for Category.

    Attributes:
        id (int): The primary key for the Category table.
        username (str): The unique username of the user.
        email (str): The unique email address of the user.
        password (str): The hashed password of the user.
    """

    __tablename__ = "dev_agnes_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    created_at = Column(DateTime, nullable=False, default=func.current_timestamp())
    updated_at = Column(DateTime, nullable=False, default=func.current_timestamp())

    devices = relationship('Device', back_populates="category")
