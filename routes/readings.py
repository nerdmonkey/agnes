import logging
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.models.reading import Reading
from app.requests.reading import ReadingCreateRequest, ReadingUpdateRequest
from app.responses.reading import (
    PaginatedReadingResponse,
    SingleReadingResponse
)
from app.services.reading import ReadingService
from config.database import get_session
from datetime import date

reading_service = ReadingService(db=None)

route = APIRouter(
    prefix="/api", tags=["Readings"], responses={404: {"description": "Not found"}}
)


@route.get("/readings", status_code=200, response_model=PaginatedReadingResponse)
async def get_readings(
    page: Optional[int] = Query(1, description="page number", gt=0),
    items_per_page: Optional[int] = Query(10, description="items per page", gt=0),
    sort_type: Optional[str] = Query('asc', description="sort type (asc or desc)"),
    sort_by: Optional[str] = Query('id', description="sort by field"),
    user_id: Optional[str] = Query(None, description="first field filter"),
    device_id: Optional[str] = Query(None, description="second field filter"),
    start_date: Optional[date] = Query(None, description="start date filter"),
    end_date: Optional[date] = Query(None, description="end date filter"),
    db: Session = Depends(get_session),
):
    """
    Get a list of readings with pagination and optional filters.

    Args:
        page (int): The page number.
        items_per_page (int): Number of items per page.
        sort_by (str): Sort by field.
        sort_type (str): Sort type (asc or desc).
        start_date (date): Start date filter.
        end_date (date): End date filter.
        user_id (str): First field filter.
        device_id (str): Second field filter.
        db (Session): SQLAlchemy database session.

    Returns:
        List[ReadingResponse]: List of reading objects.
    """
    try:
        reading_service.db = db
        items, total, last_page, first_item, last_item = reading_service.all(
            page, items_per_page, sort_type=sort_type, sort_by=sort_by,
            start_date=start_date, end_date=end_date, user_id=user_id, device_id=device_id
        )

        if not items:
            raise ValueError("No readings found")

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


@route.get("/readings/{id}", status_code=200, response_model=SingleReadingResponse)
async def get_reading(id: int, db: Session = Depends(get_session)):
    """
    Get a reading by their unique identifier.

    Args:
        id (int): The unique identifier of the reading.
        db (Session): SQLAlchemy database session.

    Returns:
        ReadingResponse: Reading object.
    """
    try:
        reading_service.db = db
        reading = reading_service.find(id)
        if not reading:
            raise HTTPException(status_code=404, detail="Reading not found")
        return {"data": reading, "status_code": 200}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@route.post("/readings", status_code=201, response_model=SingleReadingResponse)
async def create_reading(reading: ReadingCreateRequest, db: Session = Depends(get_session)):
    """
    Create a new reading.

    Args:
        reading (ReadingCreateRequest): Reading creation request.
        db (Session): SQLAlchemy database session.

    Returns:
        ReadingCreateResponse: Created reading object.

    Raises:
        HTTPException: If there is an internal server error.

    """
    try:
        reading_service.db = db
        created_reading = reading_service.save(reading)
        return {"data": created_reading, "status_code": 201}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@route.put("/readings/{id}", status_code=200, response_model=SingleReadingResponse)
async def update_reading(
    id: int, reading: ReadingUpdateRequest, db: Session = Depends(get_session)
):
    """
    Update an existing reading's information.

    Args:
        id (int): The unique identifier of the reading to update.
        reading (ReadingUpdateRequest): Reading update request.
        db (Session): SQLAlchemy database session.

    Returns:
        ReadingUpdateResponse: Updated reading object.

    Raises:
        HTTPException: If the reading is not found (status_code=404),
                       if there is a value error (status_code=400),
                       or if there is an internal server error (status_code=500).
    """
    try:
        reading_service.db = db
        updated_reading = reading_service.update(id, reading)
        if not updated_reading:
            raise HTTPException(status_code=404, detail="Reading not found")
        return {"data": updated_reading, "status_code": 200}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@route.delete("/readings/{id}", status_code=200, response_model=SingleReadingResponse)
async def delete_reading(id: int, db: Session = Depends(get_session)):
    """
    Delete a reading by their unique identifier.

    Args:
        id (int): The unique identifier of the reading to delete.
        db (Session): SQLAlchemy database session.

    Returns:
        dict: A dictionary containing the deleted reading data and the status code.

    Raises:
        HTTPException: If the reading is not found or if there is an internal server error.
    """
    try:
        reading_service.db = db

        reading = reading_service.delete(id)

        if not reading:
            raise HTTPException(status_code=500, detail="Failed to delete reading")

        return {"data": reading, "status_code": 200}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error {e}")
