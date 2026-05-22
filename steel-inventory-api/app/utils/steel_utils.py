"""Utility functions for steel product calculations and validation."""

import math
from typing import Optional

# Steel density in kg/mm^3 (approximate for carbon steel)
STEEL_DENSITY = 7.85e-6
SUPPORTED_SHAPES = {"sheet", "plate", "coil", "bar", "tube"}
_VALID_GRADES = {"A36", "304", "316", "4140"}


def _validate_positive_dimension(name: str, value: float) -> None:
    """Raise ValueError when a numeric dimension is not strictly positive."""
    if value <= 0:
        raise ValueError(f"{name} must be greater than 0")


def _normalize_shape(shape: str) -> str:
    """Normalize and validate a product shape label."""
    normalized = shape.strip().lower()
    if not normalized:
        raise ValueError("Shape must not be empty")
    if normalized not in SUPPORTED_SHAPES:
        supported = ", ".join(sorted(SUPPORTED_SHAPES))
        raise ValueError(f"Unsupported shape '{shape}'. Supported shapes: {supported}")
    return normalized


def _require_width(width_mm: Optional[float], shape: str) -> float:
    """Return validated width for shapes that require it."""
    if width_mm is None:
        raise ValueError(f"Width is required for {shape} calculations")
    _validate_positive_dimension("Width", width_mm)
    return width_mm


def calculate_sheet_weight_kg(length_mm: float, width_mm: float, thickness_mm: float) -> float:
    """Calculate sheet weight in kilograms using rectangular volume."""
    _validate_positive_dimension("Length", length_mm)
    _validate_positive_dimension("Width", width_mm)
    _validate_positive_dimension("Thickness", thickness_mm)

    volume_mm3 = length_mm * width_mm * thickness_mm
    return round(volume_mm3 * STEEL_DENSITY, 2)


def calculate_plate_weight_kg(length_mm: float, width_mm: float, thickness_mm: float) -> float:
    """Calculate plate weight in kilograms.

    A plate uses the same geometric formula as a sheet.
    """
    return calculate_sheet_weight_kg(length_mm, width_mm, thickness_mm)


def calculate_coil_weight_kg(length_mm: float, width_mm: Optional[float], thickness_mm: float) -> float:
    """Calculate coil weight in kilograms.

    Uses a rectangular approximation:
    volume = length * width * thickness.
    """
    _validate_positive_dimension("Length", length_mm)
    _validate_positive_dimension("Thickness", thickness_mm)
    width = _require_width(width_mm, "coil")

    volume_mm3 = length_mm * width * thickness_mm
    return round(volume_mm3 * STEEL_DENSITY, 2)


def calculate_bar_weight_kg(length_mm: float, width_mm: Optional[float], thickness_mm: float) -> float:
    """Calculate bar weight in kilograms.

    Uses a circular cross-section:
    volume = pi * r^2 * length.

    For bars, ``width_mm`` is interpreted as diameter.
    """
    _validate_positive_dimension("Length", length_mm)
    diameter_mm = _require_width(width_mm, "bar")
    _validate_positive_dimension("Thickness", thickness_mm)

    radius_mm = diameter_mm / 2
    area_mm2 = math.pi * (radius_mm ** 2)
    volume_mm3 = area_mm2 * length_mm
    return round(volume_mm3 * STEEL_DENSITY, 2)


def calculate_tube_weight_kg(length_mm: float, width_mm: Optional[float], thickness_mm: float) -> float:
    """Calculate tube weight in kilograms.

    Uses a hollow circular cross-section:
    volume = pi * (r_outer^2 - r_inner^2) * length.

    For tubes, ``width_mm`` is interpreted as outer diameter and
    ``thickness_mm`` as wall thickness.
    """
    _validate_positive_dimension("Length", length_mm)
    outer_diameter_mm = _require_width(width_mm, "tube")
    _validate_positive_dimension("Thickness", thickness_mm)

    outer_radius_mm = outer_diameter_mm / 2
    if thickness_mm >= outer_radius_mm:
        raise ValueError("Tube thickness must be less than outer radius")

    inner_radius_mm = outer_radius_mm - thickness_mm
    area_mm2 = math.pi * ((outer_radius_mm ** 2) - (inner_radius_mm ** 2))
    volume_mm3 = area_mm2 * length_mm
    return round(volume_mm3 * STEEL_DENSITY, 2)


def calculate_weight_kg(
    length_mm: float,
    width_mm: Optional[float],
    thickness_mm: float,
    shape: str,
) -> float:
    """Dispatch weight calculation to a shape-specific function.

    Args:
        length_mm: Product length in millimeters.
        width_mm: Product width in millimeters when required by the shape.
        thickness_mm: Product thickness in millimeters.
        shape: Supported values are sheet, plate, coil, bar, and tube.

    Returns:
        Rounded weight in kilograms.

    Raises:
        ValueError: If input dimensions or shape are invalid.
        NotImplementedError: If the shape formula is not implemented yet.
    """
    normalized_shape = _normalize_shape(shape)
    _validate_positive_dimension("Length", length_mm)
    _validate_positive_dimension("Thickness", thickness_mm)

    if normalized_shape == "sheet":
        return calculate_sheet_weight_kg(
            length_mm,
            _require_width(width_mm, normalized_shape),
            thickness_mm,
        )
    if normalized_shape == "plate":
        return calculate_plate_weight_kg(
            length_mm,
            _require_width(width_mm, normalized_shape),
            thickness_mm,
        )
    if normalized_shape == "coil":
        return calculate_coil_weight_kg(length_mm, width_mm, thickness_mm)
    if normalized_shape == "bar":
        return calculate_bar_weight_kg(length_mm, width_mm, thickness_mm)
    return calculate_tube_weight_kg(length_mm, width_mm, thickness_mm)


def validate_grade(grade: str) -> bool:
    """Return whether the supplied steel grade is recognized."""
    return grade.strip().upper() in _VALID_GRADES


def calculate_area_m2(length_mm: float, width_mm: Optional[float]) -> float:
    """Calculate rectangular area in square meters from millimeter dimensions."""
    _validate_positive_dimension("Length", length_mm)
    width = _require_width(width_mm, "area")

    area_mm2 = length_mm * width
    area_m2 = area_mm2 / 1_000_000
    return round(area_m2, 2)
