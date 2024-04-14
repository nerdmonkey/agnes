from typing import List

from pydantic import BaseModel


class UserResponse(BaseModel):
    """
    Pydantic model representing a response for a User.

    Attributes:
        id (int): The unique identifier of the user.
        username (str): The username of the user.
        email (str): The email address of the user.
    """

    id: int
    username: str
    email: str
    created_at: str
    updated_at: str


class SingleUserResponse(BaseModel):
    """
    Pydantic model representing a response for a single User.

    Attributes:
        data (UserResponse): The user response data.
        status_code (int): The HTTP status code of the response.
    """

    data: UserResponse
    status_code: int


class Pagination(BaseModel):
    """
    Pydantic model representing pagination information.

    Attributes:
        page (int): The current page number.
        items_per_page (int): The number of items per page.
        total_items (int): The total number of items.
    """

    current_page: int
    last_page: int
    first_item: int
    last_item: int
    items_per_page: int
    total: int


class PaginatedUserResponse(BaseModel):
    """
    Pydantic model representing a paginated response for a list of users.

    Attributes:
        users (List[UserResponse]): The list of users.
        pagination (Pagination): The pagination information.
    """

    data: List[UserResponse]
    meta: Pagination
    status_code: int


class UserCreateResponse(BaseModel):
    """
    Pydantic model representing a response for creating a User.

    Attributes:
        id (int): The unique identifier of the created user.
        username (str): The username of the created user.
        email (str): The email address of the created user.
    """

    id: int
    username: str
    email: str
    created_at: str
    updated_at: str


class UserUpdateResponse(BaseModel):
    """
    Pydantic model representing a response for updating a User.

    Attributes:
        id (int): The unique identifier of the updated user.
        username (str): The updated username of the user.
        email (str): The updated email address of the user.
    """

    id: int
    username: str
    email: str
    created_at: str
    updated_at: str
