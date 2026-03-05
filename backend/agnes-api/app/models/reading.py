from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.models.device import Device


from .base import Base


class Reading(Base):
    """
    Database model for Reading.

    Attributes:
        id (int): The primary key for the Reading table.
        username (str): The unique username of the user.
        email (str): The unique email address of the user.
        password (str): The hashed password of the user.
    """

    __tablename__ = "dev_agnes_readings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    device_id = Column(Integer, ForeignKey("dev_agnes_devices.id"))
    unit = Column(String)
    value = Column(String)
    created_at = Column(DateTime, nullable=False, default=func.current_timestamp())
    updated_at = Column(DateTime, nullable=False, default=func.current_timestamp())

    user = relationship('User', back_populates="readings")
    device = relationship(Device, back_populates="readings")
