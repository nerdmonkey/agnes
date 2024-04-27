from typing import List, Optional
from pydantic import BaseModel

from app.responses.device import DeviceResponse
from app.responses.user import UserResponse


class ReadingResponse(BaseModel):
    """
    Pydantic model representing a e for a user.

    Attributes:
        id (int): The unique identifier of the user.
        username (str): The username of the user.
        email (str): The email address of the user.
    """
    id: int
    user_id: int
    device_id: int
    unit: str
    value: str
    device: Optional[DeviceResponse]
    user: Optional[UserResponse]


class SingleReadingResponse(BaseModel):
    """
    Pydantic model representing a response for a single user.

    Attributes:
        data (ReadingResponse): The user response data.
        status_code (int): The HTTP status code of the response.
    """
    data: ReadingResponse
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


class PaginatedReadingResponse(BaseModel):
    """
    Pydantic model representing a paginated response for a list of users.

    Attributes:
        users (List[ReadingResponse]): The list of users.
        pagination (Pagination): The pagination information.
    """
    data: List[ReadingResponse]
    meta: Pagination
    status_code: int


class ReadingCreateResponse(BaseModel):
    """
    Pydantic model representing a response for creating a user.

    Attributes:
        id (int): The unique identifier of the created user.
        username (str): The username of the created user.
        email (str): The email address of the created user.
    """
    id: int
    user_id: int
    device_id: int
    unit: str
    value: str


class ReadingUpdateResponse(BaseModel):
    """
    Pydantic model representing a response for updating a user.

    Attributes:
        id (int): The unique identifier of the updated user.
        username (str): The updated username of the user.
        email (str): The updated email address of the user.
    """
    id: int
    user_id: int
    device_id: int
    unit: str
    value: str
