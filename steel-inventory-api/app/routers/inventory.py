from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from app.models import (
    LowStockAlertUpdateRequest,
    LowStockAlertUpdateResponse,
    SteelProduct,
    SteelProductCreate,
    SteelProductUpdate,
)
from app.database import db

router = APIRouter(
    prefix="/inventory",
    tags=["inventory"]
)

@router.get("/", response_model=List[SteelProduct])
async def get_all_products(grade: Optional[str] = None):
    """Get all products in inventory, optionally filtered by grade."""
    products = db.get_all()
    if grade is None:
        return products

    normalized_grade = grade.strip().lower()
    if not normalized_grade:
        return products

    return [
        product
        for product in products
        if product.grade.strip().lower() == normalized_grade
    ]


@router.get("/low-stock", response_model=List[SteelProduct])
async def get_low_stock_products(unsent_only: bool = False):
    """Return products whose quantity is below their minimum stock level."""
    low_stock_products = [
        product
        for product in db.get_all()
        if product.quantity < product.min_stock_level
    ]

    if unsent_only:
        low_stock_products = [
            product for product in low_stock_products if not product.alert_sent
        ]

    return low_stock_products


@router.patch("/low-stock/alerts", response_model=LowStockAlertUpdateResponse)
async def mark_low_stock_alerts_sent(payload: LowStockAlertUpdateRequest):
    """Mark alert_sent=True for a list of product IDs."""
    updated_ids, missing_ids = db.mark_alerts_sent(payload.product_ids)

    if missing_ids:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Products not found for IDs: {missing_ids}"
        )

    return LowStockAlertUpdateResponse(
        updated_count=len(updated_ids),
        product_ids=updated_ids,
    )

@router.get("/{product_id}", response_model=SteelProduct)
async def get_product(product_id: int):
    """Get a specific product by ID"""
    product = db.get_by_id(product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found"
        )
    return product

@router.post("/", response_model=SteelProduct, status_code=status.HTTP_201_CREATED)
async def create_product(product: SteelProductCreate):
    """Create a new product in inventory"""
    # TODO: Add validation using steel_utils
    product_dict = product.model_dump()
    return db.create(product_dict)

@router.patch("/{product_id}", response_model=SteelProduct)
async def update_product(product_id: int, update: SteelProductUpdate):
    """Update product quantity or location"""
    # BUG: No validation for negative quantities
    update_data = update.model_dump(exclude_unset=True)
    product = db.update(product_id, update_data)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found"
        )
    return product

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: int):
    """Delete a product from inventory"""
    if not db.delete(product_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found"
        )

# TODO: Add endpoints for:
# - Low stock alerts
# - Search/filter by grade, location, shape
# - Bulk operations
