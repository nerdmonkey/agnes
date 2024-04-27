from typing import Optional

from pydantic import BaseModel, validator


class ReadingCreateRequest(BaseModel):
    """
    Represents a Reading request.

    Attributes:
        email (str): The email name.
        price (float): The price amount.
        year (int): The fiscal year.

    Validators:
        check_decimal_places: Validates that the price has exactly 2 decimal places.
        check_year_is_integer: Validates that the fiscal year is a whole number (integer).
        check_year_range: Validates that the fiscal year is between 2023 and 2024.
    """

    user_id: int
    device_id: int
    unit: str
    value: str

    @validator("user_id", pre=True, always=True)
    def check_user_id(cls, value):
        if isinstance(value, str) and not value.strip():
            raise ValueError("The user_id field is required")

        return value

    @validator("device_id", pre=True, always=True)
    def check_device_id(cls, value):
        if isinstance(value, str) and not value.strip():
            raise ValueError("The device_id field is required")

        return value

    @validator("unit", pre=True, always=True)
    def check_unit(cls, value):
        if isinstance(value, str) and not value.strip():
            raise ValueError("The unit field is required")

        return value

    @validator("value", pre=True, always=True)
    def check_value(cls, value):
        if isinstance(value, str) and not value.strip():
            raise ValueError("The value field is required")

        return value


class ReadingUpdateRequest(BaseModel):
    """
    Data model for updating an existing Reading.

    Attributes:
        email (Optional[str]): The new email of the user. Optional.
        price (Optional[float]): The new price of the user. Optional.
        year (Optional[str]): The new year for the user. Optional.
    """

    user_id: Optional[int]
    device_id: Optional[int]
    unit: Optional[str]
    value: Optional[str]

    @validator("user_id", pre=True, always=True)
    def check_user_id(cls, value):
        if isinstance(value, str) and not value.strip():
            raise ValueError("The user_id field is required")

        return value

    @validator("device_id", pre=True, always=True)
    def check_device_id(cls, value):
        if isinstance(value, str) and not value.strip():
            raise ValueError("The device_id field is required")

        return value

    @validator("unit", pre=True, always=True)
    def check_unit(cls, value):
        if isinstance(value, str) and not value.strip():
            raise ValueError("The unit field is required")

        return value

    @validator("value", pre=True, always=True)
    def check_value(cls, value):
        if isinstance(value, str) and not value.strip():
            raise ValueError("The value field is required")

        return value
