import logging
from typing import List, Tuple

from fastapi import HTTPException
from sqlalchemy.exc import DatabaseError
from sqlalchemy.orm import Session

from app.models.device import Device
from app.requests.device import DeviceCreateRequest, DeviceUpdateRequest
from app.responses.category import CategoryResponse
from app.responses.device import DeviceCreateResponse, DeviceResponse, DeviceUpdateResponse
from app.responses.location import LocationResponse


class DeviceService:
    """
    Service class for managing device-related operations.
    """

    def __init__(self, db: Session):
        """
        Initialize the DeviceService class.

        Args:
            db (Session): The database session.
        """
        self.db = db

    def get_by_id(self, id: int) -> Device:
        """
        Retrieve a device by their ID.

        Args:
            id (int): The ID of the device.

        Returns:
            Device: The device object.

        Raises:
            HTTPException: If the device is not found.
        """
        device = self.db.query(Device).filter(Device.id == id).first()
        if not device:
            raise HTTPException(status_code=404, detail="Device not found")
        return device

    def all(self, page: int, items_per_page: int, sort_type: str = 'asc', sort_by: str = 'id', start_date: str = None, end_date: str = None, name: str = None, description: str = None) -> Tuple[List[DeviceResponse], int, int, int, int]:
        """
        Retrieve all devices with pagination and optional date, name, and second field filters.

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
            Tuple[List[DeviceResponse], int, int, int, int]: A tuple containing the list of device responses, the total number of devices, the last page number, the first item number, and the last item number.

        Raises:
            HTTPException: If there is an internal server error.
        """
        try:
            offset = (page - 1) * items_per_page

            sort_field = self.get_sort_field(sort_by)

            query = self.build_query(sort_field, sort_type, start_date, end_date, name, description)

            devices = query.offset(offset).limit(items_per_page).all()

            responses = [DeviceResponse(
                id=device.id,
                name=device.name,
                description=device.description,
                category_id=device.category_id,
                location_id=device.location_id,
                topic=device.topic,
                channel=device.channel,
                type=device.type,
                visualization=device.visualization,
                message_type=device.message_type,
                category=CategoryResponse(
                    id=device.category.id,
                    name=device.category.name,
                    description=device.category.description,
                    created_at=device.category.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    updated_at=device.category.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                ),
                location=LocationResponse(
                    id=device.location.id,
                    name=device.location.name,
                    description=device.location.description,
                    created_at=device.location.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    updated_at=device.location.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                ),
                created_at=device.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                updated_at=device.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
            ) for device in devices]

            total_devices = query.count()
            last_page = (total_devices - 1) // items_per_page + 1
            first_item = offset + 1
            last_item = min(offset + items_per_page, total_devices)

            return responses, total_devices, last_page, first_item, last_item

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
            return Device.description
        elif sort_by == 'name':
            return Device.name
        elif sort_by == 'id':
            return Device.id
        else:
            raise HTTPException(status_code=400, detail="Invalid sort_by field")

    def build_query(self, sort_field, sort_type, start_date, end_date, name, description):
        """
        Builds a query to retrieve devices based on the provided parameters.

        Args:
            sort_field (str): The field to sort the devices by.
            sort_type (str): The type of sorting, either 'asc' or 'desc'.
            start_date (str): The start date for filtering devices.
            end_date (str): The end date for filtering devices.
            name (str): The first field to filter devices by.
            description (str): The description to filter devices by.

        Returns:
            sqlalchemy.orm.query.Query: The query object for retrieving devices.
        """
        query = self.db.query(Device)

        if sort_type == 'asc':
            query = query.order_by(sort_field.asc())
        elif sort_type == 'desc':
            query = query.order_by(sort_field.desc())
        else:
            raise HTTPException(status_code=400, detail="Invalid sort_type")

        start_date = str(start_date) if start_date else ''
        end_date = str(end_date) if end_date else ''

        if start_date and end_date:
            query = query.filter(Device.created_at.between(start_date + ' 00:00:00', end_date + ' 23:59:59'))

        if name:
            query = query.filter(Device.name.like(f'%{name}%'))

        if description:
            query = query.filter(Device.description.like(f'%{description}%'))

        return query

    def total(self) -> int:
        """
        Get the total number of devices.

        Returns:
            int: The total number of devices.
        """
        return self.db.query(Device).count()

    def find(self, id: int) -> DeviceResponse:
        """
        Find a device by their ID and return the device response.

        Args:
            id (int): The ID of the device.

        Returns:
            DeviceResponse: The device response.

        Raises:
            HTTPException: If the device is not found.
        """
        device = self.get_by_id(id)
        return DeviceResponse(
            id=device.id,
            name=device.name,
            description=device.description,
            category_id=device.category_id,
            location_id=device.location_id,
            topic=device.topic,
            channel=device.channel,
            type=device.type,
            visualization=device.visualization,
            message_type=device.message_type,
            category=CategoryResponse(
                id=device.category.id,
                name=device.category.name,
                description=device.category.description,
                created_at=device.category.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                updated_at=device.category.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
            ),
            location=LocationResponse(
                id=device.location.id,
                name=device.location.name,
                description=device.location.description,
                created_at=device.location.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                updated_at=device.location.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
            ),
            created_at=device.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            updated_at=device.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
        )

    def save(self, device: DeviceCreateRequest) -> DeviceCreateResponse:
        """
        Save a new device to the database.

        Args:
            device (DeviceCreateRequest): The device create request object.

        Returns:
            DeviceCreateResponse: The response data of the created device.

        Raises:
            HTTPException: If a device with the same description already exists.
        """
        try:
            existing = self.db.query(Device).filter(Device.description == device.description).first()
            if existing:
                raise HTTPException(
                    status_code=422, detail="Device with this description already exists"
                )
            data = device.dict(exclude_unset=True)
            item = Device(**data)
            self.db.add(item)
            self.db.commit()
            self.db.refresh(item)

            item = self.db.query(Device).filter(Device.id == item.id).first()
            response_data = {
                "id": item.id,
                "name": item.name,
                "description": item.description,
                "category_id": item.category_id,
                "location_id": item.location_id,
                "topic": item.topic,
                "channel": item.channel,
                "type": item.type,
                "visualization": item.visualization,
                "message_type": item.message_type,
                "created_at": item.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "updated_at": item.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
            }
            return response_data
        except DatabaseError as e:
            logging.error(f"Error occurred while saving device: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

    def update(self, id: int, device: DeviceUpdateRequest) -> DeviceUpdateResponse:
        """
        Update a device in the database.

        Args:
            id (int): The ID of the device.
            device (DeviceUpdateRequest): The device update request object.

        Returns:
            DeviceUpdateResponse: The response data of the updated device.
        """
        try:
            item = self.get_by_id(id)
            data = device.dict(exclude_unset=True)
            if "password" in data:
                data["password"] = "hashed_" + data["password"]
            for key, value in data.items():
                setattr(item, key, value)
            self.db.commit()
            self.db.refresh(item)
            response_data = {
                "id": item.id,
                "name": item.name,
                "description": item.description,
                "category_id": item.category_id,
                "location_id": item.location_id,
                "topic": item.topic,
                "channel": item.channel,
                "type": item.type,
                "visualization": item.visualization,
                "message_type": item.message_type,
                "created_at": item.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "updated_at": item.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
            }
            return response_data
        except DatabaseError as e:
            logging.error(f"Error occurred while updating device: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

    def delete(self, id: int) -> DeviceResponse:
        """
        Deletes a device by their ID.

        Args:
            id (int): The ID of the device to delete.

        Returns:
            dict: A dictionary containing the details of the deleted device.

        Raises:
            HTTPException: If an error occurs while deleting the device.
        """
        try:
            item = self.get_by_id(id)
            self.db.delete(item)
            self.db.commit()
            response_data = {
                "id": item.id,
                "name": item.name,
                "description": item.description,
                "category_id": item.category_id,
                "location_id": item.location_id,
                "topic": item.topic,
                "channel": item.channel,
                "type": item.type,
                "visualization": item.visualization,
                "message_type": item.message_type,
                "created_at": item.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "updated_at": item.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
            }
            return response_data
        except DatabaseError as e:
            logging.error(f"Error occurred while deleting device: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")
