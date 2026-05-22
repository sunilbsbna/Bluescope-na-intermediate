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
    assert all(product["quality_grade"] == "Standard" for product in response.json())


def test_create_product_defaults_quality_grade_to_standard():
    """Create should apply the default quality grade when omitted."""
    db._seed_data()

    payload = {
        "product_code": "STL-011",
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

    response = client.post("/inventory/", json=payload)
    assert response.status_code == 201
    assert response.json()["quality_grade"] == "Standard"


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


def test_get_low_stock_products_returns_only_below_minimum():
    """Low-stock endpoint should only return products under min_stock_level."""
    response = client.get("/inventory/low-stock")
    assert response.status_code == 200

    products = response.json()
    assert len(products) > 0
    assert all(product["quantity"] < product["min_stock_level"] for product in products)


def test_get_low_stock_products_unsent_only_filter():
    """unsent_only should filter low-stock records to alerts not yet sent."""
    response = client.get("/inventory/low-stock", params={"unsent_only": True})
    assert response.status_code == 200

    products = response.json()
    assert len(products) > 0
    assert all(product["quantity"] < product["min_stock_level"] for product in products)
    assert all(product["alert_sent"] is False for product in products)


def test_patch_low_stock_alerts_marks_alert_sent():
    """PATCH low-stock alerts should mark selected products as sent."""
    db._seed_data()

    payload = {"product_ids": [2, 7]}
    response = client.patch("/inventory/low-stock/alerts", json=payload)
    assert response.status_code == 200

    response_data = response.json()
    assert response_data["updated_count"] == 2
    assert set(response_data["product_ids"]) == {2, 7}

    product_2 = db.get_by_id(2)
    product_7 = db.get_by_id(7)
    assert product_2 is not None and product_2.alert_sent is True
    assert product_7 is not None and product_7.alert_sent is True


def test_patch_low_stock_alerts_returns_404_for_missing_product_id():
    """PATCH low-stock alerts should return 404 if any ID does not exist."""
    db._seed_data()

    response = client.patch("/inventory/low-stock/alerts", json={"product_ids": [2, 999]})
    assert response.status_code == 404
    assert "Products not found" in response.json()["detail"]


def test_patch_low_stock_alerts_rejects_empty_product_ids():
    """PATCH low-stock alerts should reject empty ID lists."""
    response = client.patch("/inventory/low-stock/alerts", json={"product_ids": []})
    assert response.status_code == 422


def test_patch_low_stock_alerts_deduplicates_ids():
    """PATCH low-stock alerts should update each product at most once."""
    db._seed_data()

    response = client.patch("/inventory/low-stock/alerts", json={"product_ids": [2, 2, 2]})
    assert response.status_code == 200

    data = response.json()
    assert data["updated_count"] == 1
    assert data["product_ids"] == [2]

# TODO: Add more comprehensive tests:
# - test_create_product_success
# - test_create_product_duplicate_code
# - test_update_product_negative_quantity
# - test_delete_product
# - test_weight_calculation_sheet
# - test_weight_calculation_invalid_shape
