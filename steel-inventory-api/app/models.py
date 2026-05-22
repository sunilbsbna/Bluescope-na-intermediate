from pydantic import BaseModel, Field, model_validator
from typing import Optional, Literal
from datetime import datetime


def calculate_quality_grade(
    surface_defect_score: float,
    dimensional_accuracy: float,
    coating_uniformity: float,
) -> Literal["Premium", "Standard", "Economy"]:
    if (
        surface_defect_score < 80
        or dimensional_accuracy < 80
        or coating_uniformity < 80
    ):
        return "Economy"

    if (
        surface_defect_score >= 95
        and dimensional_accuracy >= 95
        and coating_uniformity >= 95
    ):
        return "Premium"

    return "Standard"


class CoilQualityAssessmentRequest(BaseModel):
    inspection_id: str = Field(..., min_length=1, max_length=50)
    inspected_at: datetime
    inspector_name: Optional[str] = Field(None, min_length=1, max_length=100)
    source_system: Optional[str] = Field(None, min_length=1, max_length=100)
    grading_version: str = Field(..., min_length=1, max_length=20)
    surface_defect_score: float = Field(..., ge=0, le=100)
    dimensional_accuracy_percentage: float = Field(..., ge=0, le=100)
    coating_uniformity_score: float = Field(..., ge=0, le=100)

    @model_validator(mode="after")
    def validate_inspection_source(self):
        if self.inspector_name or self.source_system:
            return self
        raise ValueError("Either inspector_name or source_system is required")


class CoilQualityAssessmentUpdate(BaseModel):
    inspection_id: Optional[str] = Field(None, min_length=1, max_length=50)
    inspected_at: Optional[datetime] = None
    inspector_name: Optional[str] = Field(None, min_length=1, max_length=100)
    source_system: Optional[str] = Field(None, min_length=1, max_length=100)
    grading_version: Optional[str] = Field(None, min_length=1, max_length=20)
    surface_defect_score: Optional[float] = Field(None, ge=0, le=100)
    dimensional_accuracy_percentage: Optional[float] = Field(None, ge=0, le=100)
    coating_uniformity_score: Optional[float] = Field(None, ge=0, le=100)


class CoilQualityAssessmentResponse(CoilQualityAssessmentRequest):
    quality_grade: Literal["Premium", "Standard", "Economy"]
    last_graded_at: datetime


class ProductQualityMetricsUpdate(BaseModel):
    surface_defect_score: float = Field(..., ge=0, le=100)
    dimensional_accuracy: float = Field(..., ge=0, le=100)
    coating_uniformity: float = Field(..., ge=0, le=100)

class SteelProduct(BaseModel):
    """Model for steel product in inventory"""
    id: Optional[int] = None
    product_code: str = Field(..., min_length=3, max_length=20)
    grade: str  # e.g., "A36", "304", "4140"
    quality_grade: Literal["Premium", "Standard", "Economy"] = "Standard"
    surface_defect_score: Optional[float] = Field(None, ge=0, le=100)
    dimensional_accuracy: Optional[float] = Field(None, ge=0, le=100)
    coating_uniformity: Optional[float] = Field(None, ge=0, le=100)
    shape: Literal["sheet", "coil", "plate", "bar", "tube"]
    length_mm: float = Field(..., gt=0)
    width_mm: Optional[float] = Field(None, gt=0)
    thickness_mm: float = Field(..., gt=0)
    quantity: int = Field(..., ge=0)
    min_stock_level: int = Field(0, ge=0)
    alert_sent: bool = False
    location: str
    coil_quality: Optional[CoilQualityAssessmentResponse] = None
    last_updated: Optional[datetime] = None

    @model_validator(mode="after")
    def populate_quality_grade(self):
        if (
            self.surface_defect_score is None
            or self.dimensional_accuracy is None
            or self.coating_uniformity is None
        ):
            return self

        self.quality_grade = calculate_quality_grade(
            self.surface_defect_score,
            self.dimensional_accuracy,
            self.coating_uniformity,
        )
        return self

    class Config:
        json_schema_extra = {
            "example": {
                "product_code": "STL-001",
                "grade": "A36",
                "quality_grade": "Standard",
                "surface_defect_score": 90,
                "dimensional_accuracy": 88,
                "coating_uniformity": 86,
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
    quality_grade: Literal["Premium", "Standard", "Economy"] = "Standard"
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
