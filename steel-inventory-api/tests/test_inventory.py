import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import db

client = TestClient(app)

def test_root_endpoint():
    """Test the root endpoint serves the frontend page."""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")
    assert "<!DOCTYPE html>" in response.text

def test_get_all_products():
    """Test getting all products"""
    response = client.get("/inventory/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_search_products_by_existing_grade():
    """Search should return only products that match an existing grade."""
    response = client.get("/inventory/", params={"grade": "A36"})
    assert response.status_code == 200

    products = response.json()
    assert len(products) > 0
    assert all(product["grade"] == "A36" for product in products)


def test_search_products_by_non_existent_grade():
    """Search should return no products when grade does not exist."""
    response = client.get("/inventory/", params={"grade": "NON_EXISTENT_GRADE"})
    assert response.status_code == 200
    assert response.json() == []


def test_search_products_by_grade_is_case_insensitive():
    """Search should return the same matches regardless of grade casing."""
    upper_response = client.get("/inventory/", params={"grade": "A36"})
    lower_response = client.get("/inventory/", params={"grade": "a36"})

    assert upper_response.status_code == 200
    assert lower_response.status_code == 200

    upper_products = upper_response.json()
    lower_products = lower_response.json()

    assert len(upper_products) > 0
    assert {product["id"] for product in upper_products} == {
        product["id"] for product in lower_products
    }


def test_search_products_empty_results_handling():
    """Search should handle empty result sets with a stable empty list response."""
    response = client.get("/inventory/", params={"grade": "ZZZ"})
    assert response.status_code == 200

    products = response.json()
    assert isinstance(products, list)
    assert len(products) == 0

# TODO: Add more comprehensive tests:
# - test_create_product_success
# - test_create_product_duplicate_code
# - test_update_product_negative_quantity
# - test_delete_product
# - test_weight_calculation_sheet
# - test_weight_calculation_invalid_shape
