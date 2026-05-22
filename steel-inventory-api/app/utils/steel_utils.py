"""Utility functions for steel calculations"""
from typing import Optional

# Steel density in kg/mm³ (approximate for carbon steel)
STEEL_DENSITY = 7.85e-6

def calculate_weight_kg(length_mm: float, width_mm: Optional[float], 
                        thickness_mm: float, shape: str) -> float:
    """
    Calculate weight of steel product in kilograms
    
    TODO: This is incomplete - needs proper formulas for different shapes
    Currently only handles sheets/plates
    """
    if shape in ["sheet", "plate"]:
        if width_mm is None:
            raise ValueError("Width required for sheets and plates")
        volume_mm3 = length_mm * width_mm * thickness_mm
        weight_kg = volume_mm3 * STEEL_DENSITY
        return round(weight_kg, 2)
    
    # TODO: Implement calculations for:
    # - coil
    # - bar (circular cross-section)
    # - tube (hollow circular cross-section)
    
    raise NotImplementedError(f"Weight calculation for {shape} not implemented yet")

def validate_grade(grade: str) -> bool:
    """
    Validate if steel grade is recognized
    
    TODO: Incomplete validation - needs more grades
    """
    valid_grades = ["A36", "304", "316", "4140"]
    return grade in valid_grades

def calculate_area_m2(length_mm: float, width_mm: Optional[float]) -> float:
    """Calculate surface area in square meters"""
    # BUG: Missing validation for None width
    area_mm2 = length_mm * width_mm
    area_m2 = area_mm2 / 1_000_000
    return round(area_m2, 2)

# TODO: Add functions for:
# - Inventory value calculation
# - Reorder point calculation
# - Optimal cutting patterns
