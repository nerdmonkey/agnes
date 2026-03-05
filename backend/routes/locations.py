import logging
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.models.location import Location
from app.requests.location import LocationCreateRequest, LocationUpdateRequest
from app.responses.location import (
    PaginatedLocationResponse,
    SingleLocationResponse
)
from app.services.location import LocationService
from config.database import get_session
from datetime import date

location_service = LocationService(db=None)

route = APIRouter(
    prefix="/api", tags=["Locations"], responses={404: {"description": "Not found"}}
)


@route.get("/locations", status_code=200, response_model=PaginatedLocationResponse)
async def get_locations(
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
    Get a list of locations with pagination and optional filters.

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
        List[LocationResponse]: List of location objects.
    """
    try:
        location_service.db = db
        items, total, last_page, first_item, last_item = location_service.all(
            page, items_per_page, sort_type=sort_type, sort_by=sort_by,
            start_date=start_date, end_date=end_date, name=name, description=description
        )

        if not items:
            raise ValueError("No locations found")

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


@route.get("/locations/{id}", status_code=200, response_model=SingleLocationResponse)
async def get_location(id: int, db: Session = Depends(get_session)):
    """
    Get a location by their unique identifier.

    Args:
        id (int): The unique identifier of the location.
        db (Session): SQLAlchemy database session.

    Returns:
        LocationResponse: Location object.
    """
    try:
        location_service.db = db
        location = location_service.find(id)
        if not location:
            raise HTTPException(status_code=404, detail="Location not found")
        return {"data": location, "status_code": 200}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@route.post("/locations", status_code=201, response_model=SingleLocationResponse)
async def create_location(location: LocationCreateRequest, db: Session = Depends(get_session)):
    """
    Create a new location.

    Args:
        location (LocationCreateRequest): Location creation request.
        db (Session): SQLAlchemy database session.

    Returns:
        LocationCreateResponse: Created location object.

    Raises:
        HTTPException: If there is an internal server error.

    """
    try:
        location_service.db = db
        created_location = location_service.save(location)
        return {"data": created_location, "status_code": 201}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@route.put("/locations/{id}", status_code=200, response_model=SingleLocationResponse)
async def update_location(
    id: int, location: LocationUpdateRequest, db: Session = Depends(get_session)
):
    """
    Update an existing location's information.

    Args:
        id (int): The unique identifier of the location to update.
        location (LocationUpdateRequest): Location update request.
        db (Session): SQLAlchemy database session.

    Returns:
        LocationUpdateResponse: Updated location object.

    Raises:
        HTTPException: If the location is not found (status_code=404),
                       if there is a value error (status_code=400),
                       or if there is an internal server error (status_code=500).
    """
    try:
        location_service.db = db
        updated_location = location_service.update(id, location)
        if not updated_location:
            raise HTTPException(status_code=404, detail="Location not found")
        return {"data": updated_location, "status_code": 200}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@route.delete("/locations/{id}", status_code=200, response_model=SingleLocationResponse)
async def delete_location(id: int, db: Session = Depends(get_session)):
    """
    Delete a location by their unique identifier.

    Args:
        id (int): The unique identifier of the location to delete.
        db (Session): SQLAlchemy database session.

    Returns:
        dict: A dictionary containing the deleted location data and the status code.

    Raises:
        HTTPException: If the location is not found or if there is an internal server error.
    """
    try:
        location_service.db = db

        location = location_service.delete(id)

        if not location:
            raise HTTPException(status_code=500, detail="Failed to delete location")

        return {"data": location, "status_code": 200}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error {e}")
