import pytest
from products.models import Product
from decimal import Decimal

@pytest.mark.django_db
class TestProductModel:
    def test_create_product(self):
        product = Product.objects.create(
            name="Test Product",
            slug="test-product",
            description="This is a test product.",
            price=Decimal("19.99"),
            is_active=True
        )

        assert product.name == "Test Product"
        assert product.slug == "test-product"
        assert product.description == "This is a test product."
        assert product.price == Decimal("19.99")
        assert product.is_active is True
        assert product.created_at is not None
    
    def test_product_str(self):
        product = Product.objects.create(
            name="Test Product",
            slug="test-product",
            description="This is a test product.",
            price=Decimal("29.99"),
            is_active=True
        )

        assert str(product) == "Test Product"