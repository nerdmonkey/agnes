from typing import Optional

from pydantic import BaseModel, field_validator


class DeviceCreateRequest(BaseModel):
    """
    Represents a Device request.

    Attributes:
        email (str): The email name.
        price (float): The price amount.
        year (int): The fiscal year.

    Validators:
        check_decimal_places: Validates that the price has exactly 2 decimal places.
        check_year_is_integer: Validates that the fiscal year is a whole number (integer).
        check_year_range: Validates that the fiscal year is between 2023 and 2024.
    """

    category_id: int
    location_id: int
    name: str
    description: str
    topic: str
    channel: int
    type: int
    visualization: int
    message_type: int

    @field_validator("category_id", mode="before")
    @classmethod
    def check_category_id(cls, value):
        if isinstance(value, str) and not value.strip():
            raise ValueError("The category_id field is required")

        return value

    @field_validator("location_id", mode="before")
    @classmethod
    def check_location_id(cls, value):
        if isinstance(value, str) and not value.strip():
            raise ValueError("The location_id field is required")

        return value

    @field_validator("topic", mode="before")
    @classmethod
    def check_topic(cls, value):
        if isinstance(value, str) and not value.strip():
            raise ValueError("The topic field is required")

        return value

    @field_validator("name", mode="before")
    @classmethod
    def check_name(cls, value):
        if isinstance(value, str) and not value.strip():
            raise ValueError("The name field is required")

        return value

    @field_validator("description", mode="before")
    @classmethod
    def check_description(cls, value):
        if isinstance(value, str) and not value.strip():
            raise ValueError("The description field is required")

        return value

    @field_validator("channel", mode="before")
    @classmethod
    def check_channel(cls, value):
        if value is None or (isinstance(value, str) and not value.strip()):
            raise ValueError("The channel field is required")
        return value

    @field_validator("type", mode="before")
    @classmethod
    def check_type(cls, value):
        if value is None or (isinstance(value, str) and not value.strip()):
            raise ValueError("The type field is required")
        return value

    @field_validator("visualization", mode="before")
    @classmethod
    def check_visualization(cls, value):
        if value is None or (isinstance(value, str) and not value.strip()):
            raise ValueError("The visualization field is required")
        return value

    @field_validator("message_type", mode="before")
    @classmethod
    def check_message_type(cls, value):
        if value is None or (isinstance(value, str) and not value.strip()):
            raise ValueError("The message_type field is required")
        return value


class DeviceUpdateRequest(BaseModel):
    """
    Data model for updating an existing Device.

    Attributes:
        email (Optional[str]): The new email of the user. Optional.
        price (Optional[float]): The new price of the user. Optional.
        year (Optional[str]): The new year for the user. Optional.
    """

    category_id: Optional[int]
    location_id: Optional[int]
    name: Optional[str]
    description: Optional[str]
    topic: Optional[str]
    channel: Optional[int]
    type: Optional[int]
    visualization: Optional[int]
    message_type: Optional[int]

    @field_validator("category_id", mode="before")
    @classmethod
    def check_category_id(cls, value):
        if isinstance(value, str) and not value.strip():
            raise ValueError("The category_id field is required")

        return value

    @field_validator("location_id", mode="before")
    @classmethod
    def check_location_id(cls, value):
        if isinstance(value, str) and not value.strip():
            raise ValueError("The location_id field is required")

        return value

    @field_validator("topic", mode="before")
    @classmethod
    def check_topic(cls, value):
        if isinstance(value, str) and not value.strip():
            raise ValueError("The topic field is required")

        return value

    @field_validator("name", mode="before")
    @classmethod
    def check_name(cls, value):
        if isinstance(value, str) and not value.strip():
            raise ValueError("The name field is required")

        return value

    @field_validator("description", mode="before")
    @classmethod
    def check_description(cls, value):
        if isinstance(value, str) and not value.strip():
            raise ValueError("The description field is required")

        return value

    @field_validator("channel", mode="before")
    @classmethod
    def check_channel(cls, value):
        if value is None or (isinstance(value, str) and not value.strip()):
            raise ValueError("The channel field is required")
        return value

    @field_validator("type", mode="before")
    @classmethod
    def check_type(cls, value):
        if value is None or (isinstance(value, str) and not value.strip()):
            raise ValueError("The type field is required")
        return value

    @field_validator("visualization", mode="before")
    @classmethod
    def check_visualization(cls, value):
        if value is None or (isinstance(value, str) and not value.strip()):
            raise ValueError("The visualization field is required")
        return value

    @field_validator("message_type", mode="before")
    @classmethod
    def check_message_type(cls, value):
        if value is None or (isinstance(value, str) and not value.strip()):
            raise ValueError("The message_type field is required")
        return value
