from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func, Text

from sqlalchemy.orm import relationship

from app.models.category import Category
from app.models.location import Location
from .base import Base


class Device(Base):
    """
    Database model for Device.

    Attributes:
        id (int): The primary key for the Device table.
        username (str): The unique username of the user.
        email (str): The unique email address of the user.
        password (str): The hashed password of the user.
    """

    __tablename__ = "dev_agnes_devices"

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("dev_agnes_categories.id"))
    location_id = Column(Integer, ForeignKey("dev_agnes_locations.id"))
    name = Column(String)
    topic = Column(String)
    description = Column(Text)
    channel = Column(Integer)
    type = Column(Integer)
    visualization = Column(Integer)
    message_type = Column(Integer)
    created_at = Column(DateTime, nullable=False, default=func.current_timestamp())
    updated_at = Column(DateTime, nullable=False, default=func.current_timestamp())

    category = relationship(Category, back_populates="devices")
    location = relationship(Location, back_populates="devices")
    readings = relationship('Reading', back_populates="device")
