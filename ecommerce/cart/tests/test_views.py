import pytest
from decimal import Decimal
from django.urls import reverse
from products.models import Product

@pytest.mark.django_db
class TestCartViews:
    def setup_method(self):
        self.product = Product.objects.create(
            name="Test Product",
            slug="test-product",
            price=Decimal("10.00"),
            is_active=True,
        )
        self.cart_detail_url = reverse("cart_detail")
        self.cart_add_url = reverse("cart_add", args=[self.product.id])
        self.cart_update_url = reverse("cart_update", args=[self.product.id])
        self.cart_remove_url = reverse("cart_remove", args=[self.product.id])
    
    def test_cart_detail_renders_empty_cart(self, client):
        response = client.get(self.cart_detail_url)

        assert response.status_code == 200
        assert response.context["cart_items"] == []
        assert response.context["total"] == 0
    
    def test_cart_add_view(self, client):
        response = client.post(self.cart_add_url, {"quantity": 2})

        assert response.status_code == 302  # Redirect to cart detail
        assert response.url == self.cart_detail_url

        response = client.get(self.cart_detail_url)

        assert len(response.context["cart_items"]) == 1
        assert response.context["cart_items"][0]["product"] == self.product
        assert response.context["cart_items"][0]["quantity"] == 2
        assert response.context["total"] == Decimal("20.00")
    
    def test_cart_update_view(self, client):
        client.post(self.cart_add_url, {"quantity": 1})

        response = client.post(self.cart_update_url, {"quantity": 5})
        cart = client.session.get("cart")

        assert response.status_code == 302  # Redirect to cart detail
        assert response.url == self.cart_detail_url
        assert cart[str(self.product.id)]["quantity"] == 5
    
    def test_cart_remove_view(self, client):
        client.post(self.cart_add_url, {"quantity": 3})

        response = client.post(self.cart_remove_url)

        assert response.status_code == 302  # Redirect to cart detail
        assert response.url == self.cart_detail_url

        response = client.get(self.cart_detail_url)

        assert response.context["cart_items"] == []
        assert response.context["total"] == 0
    
    def test_cart_add_inactive_product_404(self, client):
        inactive_product = Product.objects.create(
            name="Inactive Product",
            slug="inactive-product",
            price=Decimal("15.00"),
            is_active=False,
        )
        inactive_cart_add_url = reverse("cart_add", args=[inactive_product.id])

        response = client.post(inactive_cart_add_url, {"quantity": 1})

        assert response.status_code == 404