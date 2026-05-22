import pytest

from app.utils.steel_utils import calculate_area_m2


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
