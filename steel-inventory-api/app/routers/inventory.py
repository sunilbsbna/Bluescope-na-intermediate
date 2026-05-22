from fastapi import APIRouter, HTTPException, status
from typing import List
from app.models import SteelProduct, SteelProductCreate, SteelProductUpdate
from app.database import db

router = APIRouter(
    prefix="/inventory",
    tags=["inventory"]
)

@router.get("/", response_model=List[SteelProduct])
async def get_all_products():
    """Get all products in inventory"""
    return db.get_all()

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
