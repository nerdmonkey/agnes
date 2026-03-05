import logging
from typing import List, Tuple

from fastapi import HTTPException
from sqlalchemy.exc import DatabaseError
from sqlalchemy.orm import Session

from app.models.reading import Reading
from app.requests.reading import ReadingCreateRequest, ReadingUpdateRequest
from app.responses.category import CategoryResponse
from app.responses.device import DeviceResponse
from app.responses.location import LocationResponse
from app.responses.reading import ReadingCreateResponse, ReadingResponse, ReadingUpdateResponse
from app.responses.user import UserResponse


class ReadingService:
    """
    Service class for managing reading-related operations.
    """

    def __init__(self, db: Session):
        """
        Initialize the ReadingService class.

        Args:
            db (Session): The database session.
        """
        self.db = db

    def get_by_id(self, id: int) -> Reading:
        """
        Retrieve a reading by their ID.

        Args:
            id (int): The ID of the reading.

        Returns:
            Reading: The reading object.

        Raises:
            HTTPException: If the reading is not found.
        """
        reading = self.db.query(Reading).filter(Reading.id == id).first()
        if not reading:
            raise HTTPException(status_code=404, detail="Reading not found")
        return reading

    def all(self, page: int, items_per_page: int, sort_type: str = 'asc', sort_by: str = 'id', start_date: str = None, end_date: str = None, user_id: str = None, device_id: str = None) -> Tuple[List[ReadingResponse], int, int, int, int]:
        """
        Retrieve all readings with pagination and optional date, user_id, and second field filters.

        Args:
            page (int): The page number.
            items_per_page (int): The number of items per page.
            sort_type (str): The sort type ('asc' or 'desc').
            sort_by (str): The field to sort by ('created_at' or 'user_id').
            start_date (str): The start date for the filter (YYYY-MM-DD).
            end_date (str): The end date for the filter (YYYY-MM-DD).
            user_id (str): The first field filter.
            device_id (str): The second field filter.

        Returns:
            Tuple[List[ReadingResponse], int, int, int, int]: A tuple containing the list of reading responses, the total number of readings, the last page number, the first item number, and the last item number.

        Raises:
            HTTPException: If there is an internal server error.
        """
        try:
            offset = (page - 1) * items_per_page

            sort_field = self.get_sort_field(sort_by)

            query = self.build_query(sort_field, sort_type, start_date, end_date, user_id, device_id)

            readings = query.offset(offset).limit(items_per_page).all()

            responses = [ReadingResponse(
                id=reading.id,
                user_id=reading.user_id,
                device_id=reading.device_id,
                unit=reading.unit,
                value=reading.value,
                created_at=reading.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                updated_at=reading.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                user=UserResponse(
                    id=reading.user.id,
                    username=reading.user.username,
                    email=reading.user.email,
                    created_at=reading.user.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    updated_at=reading.user.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                ),
                device=DeviceResponse(
                    id=reading.device.id,
                    name=reading.device.name,
                    description=reading.device.description,
                    category_id=reading.device.category_id,
                    location_id=reading.device.location_id,
                    topic=reading.device.topic,
                    channel=reading.device.channel,
                    type=reading.device.type,
                    visualization=reading.device.visualization,
                    message_type=reading.device.message_type,
                    category=CategoryResponse(
                        id=reading.device.category.id,
                        name=reading.device.category.name,
                        description=reading.device.category.description,
                        created_at=reading.device.category.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                        updated_at=reading.device.category.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                    ),
                    location=LocationResponse(
                        id=reading.device.location.id,
                        name=reading.device.location.name,
                        description=reading.device.location.description,
                        created_at=reading.device.location.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                        updated_at=reading.device.location.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                    ),
                    created_at=reading.device.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    updated_at=reading.device.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                )
            ) for reading in readings]

            total_readings = query.count()
            last_page = (total_readings - 1) // items_per_page + 1
            first_item = offset + 1
            last_item = min(offset + items_per_page, total_readings)

            return responses, total_readings, last_page, first_item, last_item

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
        if sort_by == 'device_id':
            return Reading.device_id
        elif sort_by == 'user_id':
            return Reading.user_id
        elif sort_by == 'id':
            return Reading.id
        else:
            raise HTTPException(status_code=400, detail="Invalid sort_by field")

    def build_query(self, sort_field, sort_type, start_date, end_date, user_id, device_id):
        """
        Builds a query to retrieve readings based on the provided parameters.

        Args:
            sort_field (str): The field to sort the readings by.
            sort_type (str): The type of sorting, either 'asc' or 'desc'.
            start_date (str): The start date for filtering readings.
            end_date (str): The end date for filtering readings.
            user_id (str): The first field to filter readings by.
            device_id (str): The device_id to filter readings by.

        Returns:
            sqlalchemy.orm.query.Query: The query object for retrieving readings.
        """
        query = self.db.query(Reading)

        if sort_type == 'asc':
            query = query.order_by(sort_field.asc())
        elif sort_type == 'desc':
            query = query.order_by(sort_field.desc())
        else:
            raise HTTPException(status_code=400, detail="Invalid sort_type")

        start_date = str(start_date) if start_date else ''
        end_date = str(end_date) if end_date else ''

        if start_date and end_date:
            query = query.filter(Reading.created_at.between(start_date + ' 00:00:00', end_date + ' 23:59:59'))

        if user_id:
            query = query.filter(Reading.user_id.like(f'%{user_id}%'))

        if device_id:
            query = query.filter(Reading.device_id.like(f'%{device_id}%'))

        return query

    def total(self) -> int:
        """
        Get the total number of readings.

        Returns:
            int: The total number of readings.
        """
        return self.db.query(Reading).count()

    def find(self, id: int) -> ReadingResponse:
        """
        Find a reading by their ID and return the reading response.

        Args:
            id (int): The ID of the reading.

        Returns:
            ReadingResponse: The reading response.

        Raises:
            HTTPException: If the reading is not found.
        """
        reading = self.get_by_id(id)
        return ReadingResponse(
            id=reading.id,
            user_id=reading.user_id,
            device_id=reading.device_id,
            unit=reading.unit,
            value=reading.value,
            created_at=reading.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            updated_at=reading.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
            user=UserResponse(
                id=reading.user.id,
                username=reading.user.username,
                email=reading.user.email,
                created_at=reading.user.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                updated_at=reading.user.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
            ),
            device=DeviceResponse(
                id=reading.device.id,
                name=reading.device.name,
                description=reading.device.description,
                category_id=reading.device.category_id,
                location_id=reading.device.location_id,
                topic=reading.device.topic,
                channel=reading.device.channel,
                type=reading.device.type,
                visualization=reading.device.visualization,
                message_type=reading.device.message_type,
                category=CategoryResponse(
                    id=reading.device.category.id,
                    name=reading.device.category.name,
                    description=reading.device.category.description,
                    created_at=reading.device.category.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    updated_at=reading.device.category.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                ),
                location=LocationResponse(
                    id=reading.device.location.id,
                    name=reading.device.location.name,
                    description=reading.device.location.description,
                    created_at=reading.device.location.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    updated_at=reading.device.location.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                ),
                created_at=reading.device.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                updated_at=reading.device.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
            )
        )

    def save(self, reading: ReadingCreateRequest) -> ReadingCreateResponse:
        """
        Save a new reading to the database.

        Args:
            reading (ReadingCreateRequest): The reading create request object.

        Returns:
            ReadingCreateResponse: The response data of the created reading.

        Raises:
            HTTPException: If a reading with the same device_id already exists.
        """
        try:
            existing = self.db.query(Reading).filter(Reading.device_id == reading.device_id).first()
            if existing:
                raise HTTPException(
                    status_code=422, detail="Reading with this device_id already exists"
                )
            data = reading.dict(exclude_unset=True)

            item = Reading(**data)
            self.db.add(item)
            self.db.commit()
            self.db.refresh(item)

            item = self.db.query(Reading).filter(Reading.id == item.id).first()
            response_data = {
                "id": item.id,
                "user_id": item.user_id,
                "device_id": item.device_id,
                "unit": item.unit,
                "value": item.value,
                "created_at": item.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "updated_at": item.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
            }
            return response_data
        except DatabaseError as e:
            logging.error(f"Error occurred while saving reading: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

    def update(self, id: int, reading: ReadingUpdateRequest) -> ReadingUpdateResponse:
        """
        Update a reading in the database.

        Args:
            id (int): The ID of the reading.
            reading (ReadingUpdateRequest): The reading update request object.

        Returns:
            ReadingUpdateResponse: The response data of the updated reading.
        """
        try:
            item = self.get_by_id(id)
            data = reading.dict(exclude_unset=True)

            for key, value in data.items():
                setattr(item, key, value)
            self.db.commit()
            self.db.refresh(item)
            response_data = {
                "id": item.id,
                "user_id": item.user_id,
                "device_id": item.device_id,
                "unit": item.unit,
                "value": item.value,
                "created_at": item.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "updated_at": item.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
            }
            return response_data
        except DatabaseError as e:
            logging.error(f"Error occurred while updating reading: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

    def delete(self, id: int) -> ReadingResponse:
        """
        Deletes a reading by their ID.

        Args:
            id (int): The ID of the reading to delete.

        Returns:
            dict: A dictionary containing the details of the deleted reading.

        Raises:
            HTTPException: If an error occurs while deleting the reading.
        """
        try:
            item = self.get_by_id(id)
            self.db.delete(item)
            self.db.commit()
            response_data = {
                "id": item.id,
                "user_id": item.user_id,
                "device_id": item.device_id,
                "unit": item.unit,
                "value": item.value,
                "created_at": item.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "updated_at": item.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
            }
            return response_data
        except DatabaseError as e:
            logging.error(f"Error occurred while deleting reading: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")
