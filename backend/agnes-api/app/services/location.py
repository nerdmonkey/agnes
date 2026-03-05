import logging
from typing import List, Tuple

from fastapi import HTTPException
from sqlalchemy.exc import DatabaseError
from sqlalchemy.orm import Session

from app.models.location import Location
from app.requests.location import LocationCreateRequest, LocationUpdateRequest
from app.responses.location import LocationCreateResponse, LocationResponse, LocationUpdateResponse


class LocationService:
    """
    Service class for managing location-related operations.
    """

    def __init__(self, db: Session):
        """
        Initialize the LocationService class.

        Args:
            db (Session): The database session.
        """
        self.db = db

    def get_by_id(self, id: int) -> Location:
        """
        Retrieve a location by their ID.

        Args:
            id (int): The ID of the location.

        Returns:
            Location: The location object.

        Raises:
            HTTPException: If the location is not found.
        """
        location = self.db.query(Location).filter(Location.id == id).first()
        if not location:
            raise HTTPException(status_code=404, detail="Location not found")
        return location

    def all(self, page: int, items_per_page: int, sort_type: str = 'asc', sort_by: str = 'id', start_date: str = None, end_date: str = None, name: str = None, description: str = None) -> Tuple[List[LocationResponse], int, int, int, int]:
        """
        Retrieve all locations with pagination and optional date, name, and second field filters.

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
            Tuple[List[LocationResponse], int, int, int, int]: A tuple containing the list of location responses, the total number of locations, the last page number, the first item number, and the last item number.

        Raises:
            HTTPException: If there is an internal server error.
        """
        try:
            offset = (page - 1) * items_per_page

            sort_field = self.get_sort_field(sort_by)

            query = self.build_query(sort_field, sort_type, start_date, end_date, name, description)

            locations = query.offset(offset).limit(items_per_page).all()

            responses = [LocationResponse(
                id=location.id,
                name=location.name,
                description=location.description,
                created_at=location.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                updated_at=location.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
            ) for location in locations]

            total_locations = query.count()
            last_page = (total_locations - 1) // items_per_page + 1
            first_item = offset + 1
            last_item = min(offset + items_per_page, total_locations)

            return responses, total_locations, last_page, first_item, last_item

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
            return Location.description
        elif sort_by == 'name':
            return Location.name
        elif sort_by == 'id':
            return Location.id
        else:
            raise HTTPException(status_code=400, detail="Invalid sort_by field")

    def build_query(self, sort_field, sort_type, start_date, end_date, name, description):
        """
        Builds a query to retrieve locations based on the provided parameters.

        Args:
            sort_field (str): The field to sort the locations by.
            sort_type (str): The type of sorting, either 'asc' or 'desc'.
            start_date (str): The start date for filtering locations.
            end_date (str): The end date for filtering locations.
            name (str): The first field to filter locations by.
            description (str): The description to filter locations by.

        Returns:
            sqlalchemy.orm.query.Query: The query object for retrieving locations.
        """
        query = self.db.query(Location)

        if sort_type == 'asc':
            query = query.order_by(sort_field.asc())
        elif sort_type == 'desc':
            query = query.order_by(sort_field.desc())
        else:
            raise HTTPException(status_code=400, detail="Invalid sort_type")

        start_date = str(start_date) if start_date else ''
        end_date = str(end_date) if end_date else ''

        if start_date and end_date:
            query = query.filter(Location.created_at.between(start_date + ' 00:00:00', end_date + ' 23:59:59'))

        if name:
            query = query.filter(Location.name.like(f'%{name}%'))

        if description:
            query = query.filter(Location.description.like(f'%{description}%'))

        return query

    def total(self) -> int:
        """
        Get the total number of locations.

        Returns:
            int: The total number of locations.
        """
        return self.db.query(Location).count()

    def find(self, id: int) -> LocationResponse:
        """
        Find a location by their ID and return the location response.

        Args:
            id (int): The ID of the location.

        Returns:
            LocationResponse: The location response.

        Raises:
            HTTPException: If the location is not found.
        """
        location = self.get_by_id(id)
        return LocationResponse(
            id=location.id,
            name=location.name,
            description=location.description,
            created_at=location.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            updated_at=location.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
        )

    def save(self, location: LocationCreateRequest) -> LocationCreateResponse:
        """
        Save a new location to the database.

        Args:
            location (LocationCreateRequest): The location create request object.

        Returns:
            LocationCreateResponse: The response data of the created location.

        Raises:
            HTTPException: If a location with the same description already exists.
        """
        try:

            data = location.dict(exclude_unset=True)
            item = Location(**data)
            self.db.add(item)
            self.db.commit()
            self.db.refresh(item)

            item = self.db.query(Location).filter(Location.id == item.id).first()
            response_data = {
                "id": item.id,
                "name": item.name,
                "description": item.description,
                "created_at": item.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "updated_at": item.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
            }
            return response_data
        except DatabaseError as e:
            logging.error(f"Error occurred while saving location: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

    def update(self, id: int, location: LocationUpdateRequest) -> LocationUpdateResponse:
        """
        Update a location in the database.

        Args:
            id (int): The ID of the location.
            location (LocationUpdateRequest): The location update request object.

        Returns:
            LocationUpdateResponse: The response data of the updated location.
        """
        try:
            item = self.get_by_id(id)
            data = location.dict(exclude_unset=True)

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
            logging.error(f"Error occurred while updating location: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

    def delete(self, id: int) -> LocationResponse:
        """
        Deletes a location by their ID.

        Args:
            id (int): The ID of the location to delete.

        Returns:
            dict: A dictionary containing the details of the deleted location.

        Raises:
            HTTPException: If an error occurs while deleting the location.
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
            logging.error(f"Error occurred while deleting location: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")
