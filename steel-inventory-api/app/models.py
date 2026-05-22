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
    location: str

class SteelProductUpdate(BaseModel):
    quantity: Optional[int] = None
    location: Optional[str] = None
    
# TODO: Add models for batch tracking, quality inspections
