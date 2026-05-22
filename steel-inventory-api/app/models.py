from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime

class SteelProduct(BaseModel):
    """Model for steel product in inventory"""
    id: Optional[int] = None
    product_code: str = Field(..., min_length=3, max_length=20)
    grade: str  # e.g., "A36", "304", "4140"
    shape: Literal["sheet", "coil", "plate", "bar", "tube"]
    length_mm: float = Field(..., gt=0)
    width_mm: Optional[float] = Field(None, gt=0)
    thickness_mm: float = Field(..., gt=0)
    quantity: int = Field(..., ge=0)
    min_stock_level: int = Field(0, ge=0)
    alert_sent: bool = False
    location: str
    last_updated: Optional[datetime] = None

    class Config:
        json_schema_extra = {
            "example": {
                "product_code": "STL-001",
                "grade": "A36",
                "shape": "sheet",
                "length_mm": 2400,
                "width_mm": 1200,
                "thickness_mm": 6.0,
                "quantity": 150,
                "min_stock_level": 100,
                "alert_sent": False,
                "location": "Warehouse-A"
            }
        }

class SteelProductCreate(BaseModel):
    product_code: str
    grade: str
    shape: Literal["sheet", "coil", "plate", "bar", "tube"]
    length_mm: float
    width_mm: Optional[float] = None
    thickness_mm: float
    quantity: int
    min_stock_level: int = Field(0, ge=0)
    alert_sent: bool = False
    location: str

class SteelProductUpdate(BaseModel):
    quantity: Optional[int] = Field(None, ge=0)
    min_stock_level: Optional[int] = Field(None, ge=0)
    alert_sent: Optional[bool] = None
    location: Optional[str] = None


class LowStockAlertUpdateRequest(BaseModel):
    """Request payload for marking low-stock alerts as sent."""
    product_ids: list[int] = Field(..., min_length=1)


class LowStockAlertUpdateResponse(BaseModel):
    """Response body for bulk low-stock alert updates."""
    updated_count: int
    product_ids: list[int]
    
# TODO: Add models for batch tracking, quality inspections
