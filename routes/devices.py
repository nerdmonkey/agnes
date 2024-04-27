import logging
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.models.device import Device
from app.requests.device import DeviceCreateRequest, DeviceUpdateRequest
from app.responses.device import (
    PaginatedDeviceResponse,
    SingleDeviceResponse
)
from app.services.device import DeviceService
from config.database import get_session
from datetime import date

device_service = DeviceService(db=None)

route = APIRouter(
    prefix="/api", tags=["Devices"], responses={404: {"description": "Not found"}}
)


@route.get("/devices", status_code=200, response_model=PaginatedDeviceResponse)
async def get_devices(
    page: Optional[int] = Query(1, description="page number", gt=0),
    items_per_page: Optional[int] = Query(10, description="items per page", gt=0),
    sort_type: Optional[str] = Query('asc', description="sort type (asc or desc)"),
    sort_by: Optional[str] = Query('id', description="sort by field"),
    name: Optional[str] = Query(None, description="first field filter"),
    description: Optional[str] = Query(None, description="second field filter"),
    start_date: Optional[date] = Query(None, description="start date filter"),
    end_date: Optional[date] = Query(None, description="end date filter"),
    db: Session = Depends(get_session),
):
    """
    Get a list of devices with pagination and optional filters.

    Args:
        page (int): The page number.
        items_per_page (int): Number of items per page.
        sort_by (str): Sort by field.
        sort_type (str): Sort type (asc or desc).
        start_date (date): Start date filter.
        end_date (date): End date filter.
        name (str): First field filter.
        description (str): Second field filter.
        db (Session): SQLAlchemy database session.

    Returns:
        List[DeviceResponse]: List of device objects.
    """
    try:
        device_service.db = db
        items, total, last_page, first_item, last_item = device_service.all(
            page, items_per_page, sort_type=sort_type, sort_by=sort_by,
            start_date=start_date, end_date=end_date, name=name, description=description
        )

        if not items:
            raise ValueError("No devices found")

        return {
            "data": items,
            "meta": {
                "current_page": page,
                "last_page": last_page,
                "first_item": first_item,
                "last_item": last_item,
                "items_per_page": items_per_page,
                "total": total,
            },
            "status_code": 200,
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=f"{e}")
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=500, detail="Internal server error")


@route.get("/devices/{id}", status_code=200, response_model=SingleDeviceResponse)
async def get_device(id: int, db: Session = Depends(get_session)):
    """
    Get a device by their unique identifier.

    Args:
        id (int): The unique identifier of the device.
        db (Session): SQLAlchemy database session.

    Returns:
        DeviceResponse: Device object.
    """
    try:
        device_service.db = db
        device = device_service.find(id)
        if not device:
            raise HTTPException(status_code=404, detail="Device not found")
        return {"data": device, "status_code": 200}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@route.post("/devices", status_code=201, response_model=SingleDeviceResponse)
async def create_device(device: DeviceCreateRequest, db: Session = Depends(get_session)):
    """
    Create a new device.

    Args:
        device (DeviceCreateRequest): Device creation request.
        db (Session): SQLAlchemy database session.

    Returns:
        DeviceCreateResponse: Created device object.

    Raises:
        HTTPException: If there is an internal server error.

    """
    try:
        device_service.db = db
        created_device = device_service.save(device)
        return {"data": created_device, "status_code": 201}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@route.put("/devices/{id}", status_code=200, response_model=SingleDeviceResponse)
async def update_device(
    id: int, device: DeviceUpdateRequest, db: Session = Depends(get_session)
):
    """
    Update an existing device's information.

    Args:
        id (int): The unique identifier of the device to update.
        device (DeviceUpdateRequest): Device update request.
        db (Session): SQLAlchemy database session.

    Returns:
        DeviceUpdateResponse: Updated device object.

    Raises:
        HTTPException: If the device is not found (status_code=404),
                       if there is a value error (status_code=400),
                       or if there is an internal server error (status_code=500).
    """
    try:
        device_service.db = db
        updated_device = device_service.update(id, device)
        if not updated_device:
            raise HTTPException(status_code=404, detail="Device not found")
        return {"data": updated_device, "status_code": 200}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@route.delete("/devices/{id}", status_code=200, response_model=SingleDeviceResponse)
async def delete_device(id: int, db: Session = Depends(get_session)):
    """
    Delete a device by their unique identifier.

    Args:
        id (int): The unique identifier of the device to delete.
        db (Session): SQLAlchemy database session.

    Returns:
        dict: A dictionary containing the deleted device data and the status code.

    Raises:
        HTTPException: If the device is not found or if there is an internal server error.
    """
    try:
        device_service.db = db

        device = device_service.delete(id)

        if not device:
            raise HTTPException(status_code=500, detail="Failed to delete device")

        return {"data": device, "status_code": 200}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error {e}")
