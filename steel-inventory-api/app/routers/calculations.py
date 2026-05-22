from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.utils.steel_utils import calculate_weight_kg, calculate_area_m2

router = APIRouter(
    prefix="/calculations",
    tags=["calculations"]
)

class WeightRequest(BaseModel):
    length_mm: float
    width_mm: Optional[float] = None
    thickness_mm: float
    shape: str

@router.post("/weight")
async def calculate_weight(request: WeightRequest):
    """Calculate weight of steel product"""
    try:
        weight = calculate_weight_kg(
            request.length_mm,
            request.width_mm,
            request.thickness_mm,
            request.shape
        )
        return {"weight_kg": weight}
    except NotImplementedError as e:
        raise HTTPException(status_code=501, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# TODO: Add more calculation endpoints
