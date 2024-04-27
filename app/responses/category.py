from typing import List
from pydantic import BaseModel


class CategoryResponse(BaseModel):
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


class SingleCategoryResponse(BaseModel):
    """
    Pydantic model representing a response for a single user.

    Attributes:
        data (CategoryResponse): The user response data.
        status_code (int): The HTTP status code of the response.
    """
    data: CategoryResponse
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


class PaginatedCategoryResponse(BaseModel):
    """
    Pydantic model representing a paginated response for a list of users.

    Attributes:
        users (List[CategoryResponse]): The list of users.
        pagination (Pagination): The pagination information.
    """
    data: List[CategoryResponse]
    meta: Pagination
    status_code: int


class CategoryCreateResponse(BaseModel):
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


class CategoryUpdateResponse(BaseModel):
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
