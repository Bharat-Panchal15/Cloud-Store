import pytest
from decimal import Decimal
from django.urls import reverse
from products.models import Product

@pytest.mark.django_db
class TestHomeView:
    def setup_method(self):
        self.home_url = reverse('home')
        self.active_product = Product.objects.create(
            name='Active Product',
            slug='active-product',
            price=Decimal('99.99'),
            is_active=True
        )
        self.inactive_product = Product.objects.create(
            name='Inactive Product',
            slug='inactive-product',
            price=Decimal('49.99'),
            is_active=False
        )

    def test_home_view_status_code(self, client):
        response = client.get(self.home_url)

        assert response.status_code == 200

    def test_home_view_template_used(self, client):
        response = client.get(self.home_url)

        assert 'products/home.html' in (template.name for template in response.templates)

    def test_home_view_shows_only_active_products(self, client):
        response = client.get(self.home_url)

        products = response.context['products']

        assert self.active_product in products
        assert self.inactive_product not in products

    def test_home_view_context_contains_products(self, client):
        response = client.get(self.home_url)

        products = response.context['products']

        assert len(products) == 1
        assert products[0] == self.active_product