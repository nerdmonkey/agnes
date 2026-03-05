from typing import List, Optional
from pydantic import BaseModel
from app.responses.category import CategoryResponse

from app.responses.location import LocationResponse


class DeviceResponse(BaseModel):
    """
    Pydantic model representing a e for a user.

    Attributes:
        id (int): The unique identifier of the user.
        username (str): The username of the user.
        email (str): The email address of the user.
    """
    id: int
    category_id: int
    location_id: int
    name: str
    description: str
    topic: str
    channel: int
    type: int
    visualization: int
    message_type: int
    category: Optional[CategoryResponse]
    location: Optional[LocationResponse]


class SingleDeviceResponse(BaseModel):
    """
    Pydantic model representing a response for a single user.

    Attributes:
        data (DeviceResponse): The user response data.
        status_code (int): The HTTP status code of the response.
    """
    data: DeviceResponse
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


class PaginatedDeviceResponse(BaseModel):
    """
    Pydantic model representing a paginated response for a list of users.

    Attributes:
        users (List[DeviceResponse]): The list of users.
        pagination (Pagination): The pagination information.
    """
    data: List[DeviceResponse]
    meta: Pagination
    status_code: int


class DeviceCreateResponse(BaseModel):
    """
    Pydantic model representing a response for creating a user.

    Attributes:
        id (int): The unique identifier of the created user.
        username (str): The username of the created user.
        email (str): The email address of the created user.
    """
    id: int
    category_id: int
    location_id: int
    name: str
    description: str
    topic: str
    channel: int
    type: int
    visualization: int
    message_type: int


class DeviceUpdateResponse(BaseModel):
    """
    Pydantic model representing a response for updating a user.

    Attributes:
        id (int): The unique identifier of the updated user.
        username (str): The updated username of the user.
        email (str): The updated email address of the user.
    """
    id: int
    category_id: int
    location_id: int
    name: str
    description: str
    topic: str
    channel: int
    type: int
    visualization: int
    message_type: int
