from typing import List, Optional
from app.models import CoilQualityAssessmentResponse, SteelProduct
from datetime import datetime

# Simple in-memory database for the lab
# In production, this would use SQLAlchemy with a real database
class InMemoryDB:
    def __init__(self):
        self.products: List[SteelProduct] = []
        self._next_id = 1
        self._seed_data()
    
    def _seed_data(self):
        """Add some initial data"""
        sample_products = [
            SteelProduct(
                id=1,
                product_code="STL-001",
                grade="A36",
                shape="sheet",
                length_mm=2400,
                width_mm=1200,
                thickness_mm=6.0,
                quantity=150,
                min_stock_level=100,
                alert_sent=False,
                location="Warehouse-A",
                last_updated=datetime.now()
            ),
            SteelProduct(
                id=2,
                product_code="STL-002",
                grade="304",
                shape="coil",
                length_mm=5000,
                width_mm=1500,
                thickness_mm=3.0,
                quantity=75,
                min_stock_level=80,
                alert_sent=False,
                location="Warehouse-B",
                last_updated=datetime.now()
            ),
            SteelProduct(
                id=3,
                product_code="STL-003",
                grade="316",
                shape="plate",
                length_mm=3000,
                width_mm=1500,
                thickness_mm=10.0,
                quantity=50,
                min_stock_level=40,
                alert_sent=False,
                location="Warehouse-B",
                last_updated=datetime.now()
            ),
            SteelProduct(
                id=4,
                product_code="STL-004",
                grade="4140",
                shape="bar",
                length_mm=6000,
                width_mm=None,
                thickness_mm=50.0,
                quantity=200,
                min_stock_level=180,
                alert_sent=False,
                location="Warehouse-C",
                last_updated=datetime.now()
            ),
            SteelProduct(
                id=5,
                product_code="STL-005",
                grade="A36",
                shape="tube",
                length_mm=4000,
                width_mm=None,
                thickness_mm=5.0,
                quantity=120,
                min_stock_level=130,
                alert_sent=True,
                location="Warehouse-C",
                last_updated=datetime.now()
            ),
            SteelProduct(
                id=6,
                product_code="STL-006",
                grade="304",
                shape="sheet",
                length_mm=2400,
                width_mm=1200,
                thickness_mm=4.0,
                quantity=180,
                min_stock_level=150,
                alert_sent=False,
                location="Warehouse-A",
                last_updated=datetime.now()
            ),
            SteelProduct(
                id=7,
                product_code="STL-007",
                grade="A36",
                shape="plate",
                length_mm=2500,
                width_mm=1250,
                thickness_mm=12.0,
                quantity=45,
                min_stock_level=60,
                alert_sent=False,
                location="Warehouse-A",
                last_updated=datetime.now()
            ),
            SteelProduct(
                id=8,
                product_code="STL-008",
                grade="316",
                shape="coil",
                length_mm=6000,
                width_mm=1800,
                thickness_mm=2.5,
                quantity=60,
                min_stock_level=55,
                alert_sent=False,
                location="Warehouse-B",
                last_updated=datetime.now()
            ),
            SteelProduct(
                id=9,
                product_code="STL-009",
                grade="4140",
                shape="bar",
                length_mm=5000,
                width_mm=None,
                thickness_mm=40.0,
                quantity=150,
                min_stock_level=120,
                alert_sent=False,
                location="Warehouse-C",
                last_updated=datetime.now()
            ),
            SteelProduct(
                id=10,
                product_code="STL-010",
                grade="304",
                shape="tube",
                length_mm=3500,
                width_mm=None,
                thickness_mm=6.0,
                quantity=90,
                min_stock_level=95,
                alert_sent=False,
                location="Warehouse-C",
                last_updated=datetime.now()
            ),
        ]
        self.products = sample_products
        self._next_id = 11
    
    def get_all(self) -> List[SteelProduct]:
        return self.products
    
    def get_by_id(self, product_id: int) -> Optional[SteelProduct]:
        for product in self.products:
            if product.id == product_id:
                return product
        return None
    
    def create(self, product_data: dict) -> SteelProduct:
        # BUG: Missing validation for duplicate product codes
        product = SteelProduct(
            id=self._next_id,
            **product_data,
            last_updated=datetime.now()
        )
        self.products.append(product)
        self._next_id += 1
        return product
    
    def update(self, product_id: int, update_data: dict) -> Optional[SteelProduct]:
        product = self.get_by_id(product_id)
        if product:
            for key, value in update_data.items():
                if value is not None:
                    setattr(product, key, value)
            product.last_updated = datetime.now()
            return product
        return None
    
    def delete(self, product_id: int) -> bool:
        # BUG: Missing proper deletion logic
        product = self.get_by_id(product_id)
        if product:
            self.products.remove(product)
            return True
        return False

    def mark_alerts_sent(self, product_ids: List[int]) -> tuple[List[int], List[int]]:
        """Mark alerts as sent for matching product IDs.

        Returns a tuple of (updated_ids, missing_ids).
        """
        updated_ids: List[int] = []
        missing_ids: List[int] = []
        seen_ids: set[int] = set()

        for product_id in product_ids:
            if product_id in seen_ids:
                continue
            seen_ids.add(product_id)

            product = self.get_by_id(product_id)
            if product is None:
                missing_ids.append(product_id)
                continue

            product.alert_sent = True
            product.last_updated = datetime.now()
            updated_ids.append(product_id)

        return updated_ids, missing_ids

    def get_coil_quality_assessment(
        self, product_id: int
    ) -> Optional[CoilQualityAssessmentResponse]:
        product = self.get_by_id(product_id)
        if product is None:
            return None
        return product.coil_quality

    def save_coil_quality_assessment(
        self, product_id: int, assessment_data: dict
    ) -> Optional[CoilQualityAssessmentResponse]:
        product = self.get_by_id(product_id)
        if product is None:
            return None

        assessment = CoilQualityAssessmentResponse(**assessment_data)
        product.coil_quality = assessment
        product.quality_grade = assessment.quality_grade
        product.last_updated = datetime.now()
        return assessment

# Global database instance
db = InMemoryDB()
