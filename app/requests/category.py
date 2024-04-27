from typing import Optional

from pydantic import BaseModel, validator


class CategoryCreateRequest(BaseModel):
    """
    Represents a Category request.

    Attributes:
        email (str): The email name.
        price (float): The price amount.
        year (int): The fiscal year.

    Validators:
        check_decimal_places: Validates that the price has exactly 2 decimal places.
        check_year_is_integer: Validates that the fiscal year is a whole number (integer).
        check_year_range: Validates that the fiscal year is between 2023 and 2024.
    """

    name: str
    description: str

    @validator("name", pre=True, always=True)
    def check_name(cls, value):
        if not value.strip():
            raise ValueError("The name field is required")

        return value

    @validator("description", pre=True, always=True)
    def check_description(cls, value):
        if not value.strip():
            raise ValueError("The description field is required")

        return value


class CategoryUpdateRequest(BaseModel):
    """
    Data model for updating an existing Category.

    Attributes:
        email (Optional[str]): The new email of the user. Optional.
        price (Optional[float]): The new price of the user. Optional.
        year (Optional[str]): The new year for the user. Optional.
    """

    name: Optional[str]
    description: Optional[str]

    @validator("name", pre=True, always=True)
    def check_name(cls, value):
        if not value.strip():
            raise ValueError("The name field is required")

        return value

    @validator("description", pre=True, always=True)
    def check_description(cls, value):
        if not value.strip():
            raise ValueError("The description field is required")

        return value
