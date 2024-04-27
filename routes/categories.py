import logging
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.models.category import Category
from app.requests.category import CategoryCreateRequest, CategoryUpdateRequest
from app.responses.category import (
    PaginatedCategoryResponse,
    SingleCategoryResponse
)
from app.services.category import CategoryService
from config.database import get_session
from datetime import date

category_service = CategoryService(db=None)

route = APIRouter(
    prefix="/api", tags=["Categories"], responses={404: {"description": "Not found"}}
)


@route.get("/categories", status_code=200, response_model=PaginatedCategoryResponse)
async def get_categories(
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
    Get a list of categories with pagination and optional filters.

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
        List[CategoryResponse]: List of category objects.
    """
    try:
        category_service.db = db
        items, total, last_page, first_item, last_item = category_service.all(
            page, items_per_page, sort_type=sort_type, sort_by=sort_by,
            start_date=start_date, end_date=end_date, name=name, description=description
        )

        if not items:
            raise ValueError("No categories found")

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


@route.get("/categories/{id}", status_code=200, response_model=SingleCategoryResponse)
async def get_category(id: int, db: Session = Depends(get_session)):
    """
    Get a category by their unique identifier.

    Args:
        id (int): The unique identifier of the category.
        db (Session): SQLAlchemy database session.

    Returns:
        CategoryResponse: Category object.
    """
    try:
        category_service.db = db
        category = category_service.find(id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        return {"data": category, "status_code": 200}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@route.post("/categories", status_code=201, response_model=SingleCategoryResponse)
async def create_category(category: CategoryCreateRequest, db: Session = Depends(get_session)):
    """
    Create a new category.

    Args:
        category (CategoryCreateRequest): Category creation request.
        db (Session): SQLAlchemy database session.

    Returns:
        CategoryCreateResponse: Created category object.

    Raises:
        HTTPException: If there is an internal server error.

    """
    try:
        category_service.db = db
        created_category = category_service.save(category)
        return {"data": created_category, "status_code": 201}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@route.put("/categories/{id}", status_code=200, response_model=SingleCategoryResponse)
async def update_category(
    id: int, category: CategoryUpdateRequest, db: Session = Depends(get_session)
):
    """
    Update an existing category's information.

    Args:
        id (int): The unique identifier of the category to update.
        category (CategoryUpdateRequest): Category update request.
        db (Session): SQLAlchemy database session.

    Returns:
        CategoryUpdateResponse: Updated category object.

    Raises:
        HTTPException: If the category is not found (status_code=404),
                       if there is a value error (status_code=400),
                       or if there is an internal server error (status_code=500).
    """
    try:
        category_service.db = db
        updated_category = category_service.update(id, category)
        if not updated_category:
            raise HTTPException(status_code=404, detail="Category not found")
        return {"data": updated_category, "status_code": 200}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@route.delete("/categories/{id}", status_code=200, response_model=SingleCategoryResponse)
async def delete_category(id: int, db: Session = Depends(get_session)):
    """
    Delete a category by their unique identifier.

    Args:
        id (int): The unique identifier of the category to delete.
        db (Session): SQLAlchemy database session.

    Returns:
        dict: A dictionary containing the deleted category data and the status code.

    Raises:
        HTTPException: If the category is not found or if there is an internal server error.
    """
    try:
        category_service.db = db

        category = category_service.delete(id)

        if not category:
            raise HTTPException(status_code=500, detail="Failed to delete category")

        return {"data": category, "status_code": 200}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error {e}")
