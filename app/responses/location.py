from typing import List
from pydantic import BaseModel


class LocationResponse(BaseModel):
    """
    Pydantic model representing a e for a user.

    Attributes:
        id (int): The unique identifier of the user.
        username (str): The username of the user.
        email (str): The email address of the user.
    """
    id: int
    name: str
    description: str


class SingleLocationResponse(BaseModel):
    """
    Pydantic model representing a response for a single user.

    Attributes:
        data (LocationResponse): The user response data.
        status_code (int): The HTTP status code of the response.
    """
    data: LocationResponse
    status_code: int


class Pagination(BaseModel):
    """
    Pydantic model representing pagination information.

    Attributes:
        current_page (int): The current page number.
        items_per_current_page (int): The number of items per page.
        total_items (int): The total number of items.
    """
    current_page: int
    last_page: int
    first_item: int
    last_item: int
    items_per_page: int
    total: int


class PaginatedLocationResponse(BaseModel):
    """
    Pydantic model representing a paginated response for a list of users.

    Attributes:
        users (List[LocationResponse]): The list of users.
        pagination (Pagination): The pagination information.
    """
    data: List[LocationResponse]
    meta: Pagination
    status_code: int


class LocationCreateResponse(BaseModel):
    """
    Pydantic model representing a response for creating a user.

    Attributes:
        id (int): The unique identifier of the created user.
        username (str): The username of the created user.
        email (str): The email address of the created user.
    """
    id: int
    name: str
    description: str


class LocationUpdateResponse(BaseModel):
    """
    Pydantic model representing a response for updating a user.

    Attributes:
        id (int): The unique identifier of the updated user.
        username (str): The updated username of the user.
        email (str): The updated email address of the user.
    """
    id: int
    name: str
    description: str
