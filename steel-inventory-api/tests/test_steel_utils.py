import pytest

from app.utils.steel_utils import calculate_area_m2, calculate_weight_kg, validate_grade


def test_calculate_area_m2_valid_dimensions():
    assert calculate_area_m2(2000, 1000) == 2.0


def test_calculate_area_m2_raises_for_none_width():
    with pytest.raises(ValueError, match="Width is required"):
        calculate_area_m2(2000, None)


def test_calculate_area_m2_raises_for_non_positive_length():
    with pytest.raises(ValueError, match="Length must be greater than 0"):
        calculate_area_m2(0, 1000)


def test_calculate_area_m2_raises_for_non_positive_width():
    with pytest.raises(ValueError, match="Width must be greater than 0"):
        calculate_area_m2(2000, -1)


def test_calculate_weight_kg_for_sheet():
    assert calculate_weight_kg(2000, 1000, 10, "sheet") == 157.0


def test_calculate_weight_kg_for_plate_case_insensitive_shape():
    assert calculate_weight_kg(1000, 500, 10, "Plate") == 39.25


def test_calculate_weight_kg_raises_for_unsupported_shape():
    with pytest.raises(ValueError, match="Unsupported shape"):
        calculate_weight_kg(1000, 500, 10, "angle")


def test_calculate_weight_kg_raises_for_missing_width_sheet():
    with pytest.raises(ValueError, match="Width is required for sheet calculations"):
        calculate_weight_kg(1000, None, 10, "sheet")


def test_calculate_weight_kg_raises_for_non_positive_thickness():
    with pytest.raises(ValueError, match="Thickness must be greater than 0"):
        calculate_weight_kg(1000, 500, 0, "sheet")


def test_calculate_weight_kg_for_coil_rectangular_approximation():
    assert calculate_weight_kg(2000, 1000, 1, "coil") == 15.7


def test_calculate_weight_kg_for_bar_circular_cross_section():
    assert calculate_weight_kg(1000, 20, 10, "bar") == 2.47


def test_calculate_weight_kg_for_tube_hollow_cross_section():
    assert calculate_weight_kg(1000, 40, 2, "tube") == 1.87


def test_calculate_weight_kg_tube_raises_for_excessive_thickness():
    with pytest.raises(ValueError, match="less than outer radius"):
        calculate_weight_kg(1000, 20, 10, "tube")


def test_validate_grade_normalizes_case_and_whitespace():
    assert validate_grade("  a36 ") is True
    assert validate_grade("x70") is False
