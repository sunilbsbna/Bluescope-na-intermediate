import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import db

client = TestClient(app)

def test_root_endpoint():
    """Test the root endpoint returns welcome message"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_get_all_products():
    """Test getting all products"""
    response = client.get("/inventory/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# TODO: Add more comprehensive tests:
# - test_create_product_success
# - test_create_product_duplicate_code
# - test_update_product_negative_quantity
# - test_delete_product
# - test_weight_calculation_sheet
# - test_weight_calculation_invalid_shape
