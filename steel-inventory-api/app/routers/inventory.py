from fastapi import APIRouter, HTTPException, status
from datetime import datetime, timezone
from typing import List, Optional
from app.models import (
    CoilQualityAssessmentRequest,
    CoilQualityAssessmentResponse,
    CoilQualityAssessmentUpdate,
    ProductQualityMetricsUpdate,
    LowStockAlertUpdateRequest,
    LowStockAlertUpdateResponse,
    SteelProduct,
    SteelProductCreate,
    SteelProductUpdate,
    calculate_quality_grade,
)
from app.database import db

router = APIRouter(
    prefix="/inventory",
    tags=["inventory"]
)


def _get_existing_product_or_404(product_id: int):
    product = db.get_by_id(product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found"
        )
    return product


def _require_coil_product(product_id: int):
    product = _get_existing_product_or_404(product_id)
    if product.shape != "coil":
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Coil grading is only supported for products with shape 'coil'"
        )
    return product


def _build_grading_response(
    payload: CoilQualityAssessmentRequest,
) -> CoilQualityAssessmentResponse:
    return CoilQualityAssessmentResponse(
        **payload.model_dump(),
        quality_grade=calculate_quality_grade(
            payload.surface_defect_score,
            payload.dimensional_accuracy_percentage,
            payload.coating_uniformity_score,
        ),
        last_graded_at=datetime.now(timezone.utc),
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
    return _get_existing_product_or_404(product_id)


@router.post("/{product_id}/grade", response_model=SteelProduct)
async def grade_product(
    product_id: int,
    payload: ProductQualityMetricsUpdate,
):
    """Update a coil product with summarized quality metrics and its grade."""
    _require_coil_product(product_id)

    update_data = payload.model_dump()
    update_data["quality_grade"] = calculate_quality_grade(
        payload.surface_defect_score,
        payload.dimensional_accuracy,
        payload.coating_uniformity,
    )

    product = db.update(product_id, update_data)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found"
        )

    return product


@router.post("/{product_id}/grading", response_model=CoilQualityAssessmentResponse)
async def create_coil_grading(
    product_id: int,
    payload: CoilQualityAssessmentRequest,
):
    """Create or replace the grading assessment for a coil product."""
    _require_coil_product(product_id)

    assessment = _build_grading_response(payload)
    return db.save_coil_quality_assessment(product_id, assessment.model_dump())


@router.get("/{product_id}/grading", response_model=CoilQualityAssessmentResponse)
async def get_coil_grading(product_id: int):
    """Return the latest grading assessment for a coil product."""
    _require_coil_product(product_id)

    assessment = db.get_coil_quality_assessment(product_id)
    if assessment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} does not have a grading assessment"
        )

    return assessment


@router.patch("/{product_id}/grading", response_model=CoilQualityAssessmentResponse)
async def update_coil_grading(
    product_id: int,
    update: CoilQualityAssessmentUpdate,
):
    """Update a coil grading assessment and recompute the business grade."""
    _require_coil_product(product_id)

    existing_assessment = db.get_coil_quality_assessment(product_id)
    if existing_assessment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} does not have a grading assessment"
        )

    merged_payload = existing_assessment.model_dump(
        exclude={"quality_grade", "last_graded_at"}
    )
    merged_payload.update(update.model_dump(exclude_unset=True))

    assessment_request = CoilQualityAssessmentRequest(**merged_payload)
    assessment = _build_grading_response(assessment_request)
    return db.save_coil_quality_assessment(product_id, assessment.model_dump())

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
