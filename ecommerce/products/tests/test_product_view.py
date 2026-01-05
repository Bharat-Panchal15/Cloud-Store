import pytest
from decimal import Decimal
from django.urls import reverse
from products.models import Product

@pytest.mark.django_db
class TestProductView:
    def setup_method(self):
        self.active_product = Product.objects.create(
            name="Active Product",
            slug="active-product",
            price=Decimal("99.99"),
            is_active=True,
        )
        self.inactive_product = Product.objects.create(
            name="Inactive Product",
            slug="inactive-product",
            price=Decimal("199.99"),
            is_active=False,
        )
    
    def test_product_detail_view_status_code_active(self, client):
        url = reverse('product_detail', args=[self.active_product.slug])
        response = client.get(url)

        assert response.status_code == 200
        assert response.context['product'] == self.active_product
    
    def test_product_detail_view_status_code_inactive(self, client):
        url = reverse('product_detail', args=[self.inactive_product.slug])
        response = client.get(url)

        assert response.status_code == 404
    
    def test_product_detail_view_template_used(self, client):
        url = reverse('product_detail', args=[self.active_product.slug])
        response = client.get(url)

        assert 'products/product.html' in (template.name for template in response.templates)
    
    def test_product_detail_view_404_for_nonexistent_product(self, client):
        url = reverse('product_detail', args=['nonexistent-product'])
        response = client.get(url)

        assert response.status_code == 404