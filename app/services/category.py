import logging
from typing import List, Tuple

from fastapi import HTTPException
from sqlalchemy.exc import DatabaseError
from sqlalchemy.orm import Session

from app.models.category import Category
from app.requests.category import CategoryCreateRequest, CategoryUpdateRequest
from app.responses.category import CategoryCreateResponse, CategoryResponse, CategoryUpdateResponse


class CategoryService:
    """
    Service class for managing category-related operations.
    """

    def __init__(self, db: Session):
        """
        Initialize the CategoryService class.

        Args:
            db (Session): The database session.
        """
        self.db = db

    def get_by_id(self, id: int) -> Category:
        """
        Retrieve a category by their ID.

        Args:
            id (int): The ID of the category.

        Returns:
            Category: The category object.

        Raises:
            HTTPException: If the category is not found.
        """
        category = self.db.query(Category).filter(Category.id == id).first()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        return category

    def all(self, page: int, items_per_page: int, sort_type: str = 'asc', sort_by: str = 'id', start_date: str = None, end_date: str = None, name: str = None, description: str = None) -> Tuple[List[CategoryResponse], int, int, int, int]:
        """
        Retrieve all categorys with pagination and optional date, name, and second field filters.

        Args:
            page (int): The page number.
            items_per_page (int): The number of items per page.
            sort_type (str): The sort type ('asc' or 'desc').
            sort_by (str): The field to sort by ('created_at' or 'name').
            start_date (str): The start date for the filter (YYYY-MM-DD).
            end_date (str): The end date for the filter (YYYY-MM-DD).
            name (str): The first field filter.
            description (str): The second field filter.

        Returns:
            Tuple[List[CategoryResponse], int, int, int, int]: A tuple containing the list of category responses, the total number of categorys, the last page number, the first item number, and the last item number.

        Raises:
            HTTPException: If there is an internal server error.
        """
        try:
            offset = (page - 1) * items_per_page

            sort_field = self.get_sort_field(sort_by)

            query = self.build_query(sort_field, sort_type, start_date, end_date, name, description)

            categorys = query.offset(offset).limit(items_per_page).all()

            responses = [CategoryResponse(
                id=category.id,
                name=category.name,
                description=category.description,
                created_at=category.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                updated_at=category.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
            ) for category in categorys]

            total_categorys = query.count()
            last_page = (total_categorys - 1) // items_per_page + 1
            first_item = offset + 1
            last_item = min(offset + items_per_page, total_categorys)

            return responses, total_categorys, last_page, first_item, last_item

        except DatabaseError:
            raise HTTPException(status_code=500, detail="Internal server error")

    def get_sort_field(self, sort_by: str):
        """
        Returns the corresponding sort field based on the given sort_by parameter.

        Args:
            sort_by (str): The field to sort by.

        Returns:
            The sort field corresponding to the given sort_by parameter.

        Raises:
            HTTPException: If the sort_by field is invalid.
        """
        if sort_by == 'description':
            return Category.description
        elif sort_by == 'name':
            return Category.name
        elif sort_by == 'id':
            return Category.id
        else:
            raise HTTPException(status_code=400, detail="Invalid sort_by field")

    def build_query(self, sort_field, sort_type, start_date, end_date, name, description):
        """
        Builds a query to retrieve categorys based on the provided parameters.

        Args:
            sort_field (str): The field to sort the categorys by.
            sort_type (str): The type of sorting, either 'asc' or 'desc'.
            start_date (str): The start date for filtering categorys.
            end_date (str): The end date for filtering categorys.
            name (str): The first field to filter categorys by.
            description (str): The description to filter categorys by.

        Returns:
            sqlalchemy.orm.query.Query: The query object for retrieving categorys.
        """
        query = self.db.query(Category)

        if sort_type == 'asc':
            query = query.order_by(sort_field.asc())
        elif sort_type == 'desc':
            query = query.order_by(sort_field.desc())
        else:
            raise HTTPException(status_code=400, detail="Invalid sort_type")

        start_date = str(start_date) if start_date else ''
        end_date = str(end_date) if end_date else ''

        if start_date and end_date:
            query = query.filter(Category.created_at.between(start_date + ' 00:00:00', end_date + ' 23:59:59'))

        if name:
            query = query.filter(Category.name.like(f'%{name}%'))

        if description:
            query = query.filter(Category.description.like(f'%{description}%'))

        return query

    def total(self) -> int:
        """
        Get the total number of categorys.

        Returns:
            int: The total number of categorys.
        """
        return self.db.query(Category).count()

    def find(self, id: int) -> CategoryResponse:
        """
        Find a category by their ID and return the category response.

        Args:
            id (int): The ID of the category.

        Returns:
            CategoryResponse: The category response.

        Raises:
            HTTPException: If the category is not found.
        """
        category = self.get_by_id(id)
        return CategoryResponse(
            id=category.id,
            name=category.name,
            description=category.description,
            created_at=category.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            updated_at=category.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
        )

    def save(self, category: CategoryCreateRequest) -> CategoryCreateResponse:
        """
        Save a new category to the database.

        Args:
            category (CategoryCreateRequest): The category create request object.

        Returns:
            CategoryCreateResponse: The response data of the created category.

        Raises:
            HTTPException: If a category with the same description already exists.
        """
        try:

            data = category.dict(exclude_unset=True)
            item = Category(**data)
            self.db.add(item)
            self.db.commit()
            self.db.refresh(item)

            item = self.db.query(Category).filter(Category.id == item.id).first()
            response_data = {
                "id": item.id,
                "name": item.name,
                "description": item.description,
                "created_at": item.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "updated_at": item.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
            }
            return response_data
        except DatabaseError as e:
            logging.error(f"Error occurred while saving category: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

    def update(self, id: int, category: CategoryUpdateRequest) -> CategoryUpdateResponse:
        """
        Update a category in the database.

        Args:
            id (int): The ID of the category.
            category (CategoryUpdateRequest): The category update request object.

        Returns:
            CategoryUpdateResponse: The response data of the updated category.
        """
        try:
            item = self.get_by_id(id)
            data = category.dict(exclude_unset=True)

            for key, value in data.items():
                setattr(item, key, value)
            self.db.commit()
            self.db.refresh(item)
            response_data = {
                "id": item.id,
                "name": item.name,
                "description": item.description,
                "created_at": item.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "updated_at": item.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
            }
            return response_data
        except DatabaseError as e:
            logging.error(f"Error occurred while updating category: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

    def delete(self, id: int) -> CategoryResponse:
        """
        Deletes a category by their ID.

        Args:
            id (int): The ID of the category to delete.

        Returns:
            dict: A dictionary containing the details of the deleted category.

        Raises:
            HTTPException: If an error occurs while deleting the category.
        """
        try:
            item = self.get_by_id(id)
            self.db.delete(item)
            self.db.commit()
            response_data = {
                "id": item.id,
                "name": item.name,
                "description": item.description,
                "created_at": item.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "updated_at": item.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
            }
            return response_data
        except DatabaseError as e:
            logging.error(f"Error occurred while deleting category: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")
