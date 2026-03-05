import logging
from typing import List, Tuple, Union

from fastapi import HTTPException
from sqlalchemy.exc import DatabaseError
from sqlalchemy.orm import Session

from app.models.user import User
from app.requests.user import UserCreateRequest, UserUpdateRequest
from app.responses.user import UserCreateResponse, UserResponse, UserUpdateResponse


class UserService:
    """
    Service class for managing user-related operations.
    """

    def __init__(self, db: Session):
        """
        Initialize the UserService class.

        Args:
            db (Session): The database session.
        """
        self.db = db

    def get_by_id(self, id: int) -> User:
        """
        Retrieve a user by their ID.

        Args:
            id (int): The ID of the user.

        Returns:
            User: The user object.

        Raises:
            HTTPException: If the user is not found.
        """
        user = self.db.query(User).filter(User.id == id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    def all(
        self,
        page: int,
        items_per_page: int,
        sort_type: str = "asc",
        sort_by: str = "id",
        start_date: str = None,
        end_date: str = None,
        username: str = None,
        email: str = None,
    ) -> Tuple[List[UserResponse], int, int, int, int]:
        """
        Retrieve all users with pagination and optional date, username, and email filters.

        Args:
            page (int): The page number.
            items_per_page (int): The number of items per page.
            sort_type (str): The sort type ('asc' or 'desc').
            sort_by (str): The field to sort by ('created_at' or 'username').
            start_date (str): The start date for the filter (YYYY-MM-DD).
            end_date (str): The end date for the filter (YYYY-MM-DD).
            username (str): The username filter.
            email (str): The email filter.

        Returns:
            Tuple[List[UserResponse], int, int, int, int]: A tuple containing the list of user responses,
            the total number of users, the last page number, the first item number, and the last item number.

        Raises:
            HTTPException: If there is an internal server error.
        """
        try:
            offset = (page - 1) * items_per_page

            sort_field = self.get_sort_field(sort_by)

            query = self.build_query(
                sort_field, sort_type, start_date, end_date, username, email
            )

            users = query.offset(offset).limit(items_per_page).all()

            responses = [
                UserResponse(
                    id=user.id,
                    username=user.username,
                    email=user.email,
                    created_at=user.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    updated_at=user.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                )
                for user in users
            ]

            total_users = query.count()
            last_page = (total_users - 1) // items_per_page + 1
            first_item = offset + 1
            last_item = min(offset + items_per_page, total_users)

            return responses, total_users, last_page, first_item, last_item

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
        if sort_by == "email":
            return User.email
        elif sort_by == "username":
            return User.username
        elif sort_by == "id":
            return User.id
        else:
            raise HTTPException(status_code=400, detail="Invalid sort_by field")

    def build_query(self, sort_field, sort_type, start_date, end_date, username, email):
        """
        Builds a query to retrieve users based on the provided parameters.

        Args:
            sort_field (str): The field to sort the users by.
            sort_type (str): The type of sorting, either 'asc' or 'desc'.
            start_date (str): The start date for filtering users.
            end_date (str): The end date for filtering users.
            username (str): The username to filter users by.
            email (str): The email to filter users by.

        Returns:
            sqlalchemy.orm.query.Query: The query object for retrieving users.
        """
        query = self.db.query(User)

        if sort_type == "asc":
            query = query.order_by(sort_field.asc())
        elif sort_type == "desc":
            query = query.order_by(sort_field.desc())
        else:
            raise HTTPException(status_code=400, detail="Invalid sort_type")

        start_date = str(start_date) if start_date else ""
        end_date = str(end_date) if end_date else ""

        if start_date and end_date:
            query = query.filter(
                User.created_at.between(
                    start_date + " 00:00:00", end_date + " 23:59:59"
                )
            )

        if username:
            query = query.filter(User.username.like(f"%{username}%"))

        if email:
            query = query.filter(User.email.like(f"%{email}%"))

        return query

    def total(self) -> int:
        """
        Get the total number of users.

        Returns:
            int: The total number of users.
        """
        return self.db.query(User).count()

    def find(self, id: int) -> UserResponse:
        """
        Find a user by their ID and return the user response.

        Args:
            id (int): The ID of the user.

        Returns:
            UserResponse: The user response.

        Raises:
            HTTPException: If the user is not found.
        """
        user = self.get_by_id(id)
        return UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            created_at=user.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            updated_at=user.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
        )

    def save(self, user: UserCreateRequest) -> UserCreateResponse:
        """
        Save a new user to the database.

        Args:
            user (UserCreateRequest): The user create request object.

        Returns:
            UserCreateResponse: The response data of the created user.

        Raises:
            HTTPException: If a user with the same email already exists.
        """
        try:
            existing = self.db.query(User).filter(User.email == user.email).first()
            if existing:
                raise HTTPException(
                    status_code=422, detail="User with this email already exists"
                )
            data = user.dict(exclude_unset=True)
            data["password"] = "hashed_" + data["password"]
            item = User(**data)
            self.db.add(item)
            self.db.commit()
            self.db.refresh(item)

            item = self.db.query(User).filter(User.id == item.id).first()
            response_data = {
                "id": item.id,
                "username": item.username,
                "email": item.email,
                "created_at": item.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "updated_at": item.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
            }
            return response_data
        except DatabaseError as e:
            logging.error(f"Error occurred while saving user: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

    def update(self, id: int, user: UserUpdateRequest) -> UserUpdateResponse:
        """
        Update a user in the database.

        Args:
            id (int): The ID of the user.
            user (UserUpdateRequest): The user update request object.

        Returns:
            UserUpdateResponse: The response data of the updated user.
        """
        try:
            item = self.get_by_id(id)
            data = user.dict(exclude_unset=True)
            if "password" in data:
                data["password"] = "hashed_" + data["password"]
            for key, value in data.items():
                setattr(item, key, value)
            self.db.commit()
            self.db.refresh(item)
            response_data = {
                "id": item.id,
                "username": item.username,
                "email": item.email,
                "created_at": item.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "updated_at": item.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
            }
            return response_data
        except DatabaseError as e:
            logging.error(f"Error occurred while updating user: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

    def delete(self, id: int) -> UserResponse:
        try:
            item = self.get_by_id(id)
            response_data = {
                "id": item.id,
                "username": item.username,
                "email": item.email,
                "created_at": item.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "updated_at": item.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
            }
            self.db.delete(item)
            self.db.commit()
            return response_data
        except DatabaseError as e:
            logging.error(f"Error occurred while deleting user: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

    def bulk_delete(self, ids: Union[int, List[int]]):
        if isinstance(ids, int):
            ids = [ids]

        deleted_users = []

        for id in ids:
            item = self.get_by_id(id)
            if item:
                self.db.delete(item)
                response_data = {
                    "id": item.id,
                    "username": item.username,
                    "email": item.email,
                    "created_at": item.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    "updated_at": item.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                }
                deleted_users.append(response_data)

        self.db.commit()

        response_data = deleted_users

        return response_data
