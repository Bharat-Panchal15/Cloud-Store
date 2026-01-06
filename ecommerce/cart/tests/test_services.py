import pytest
from decimal import Decimal
from django.test import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from cart.services import *
from products.models import Product

@pytest.mark.django_db
class TestCartServices:
    def setup_method(self):
        self.factory = RequestFactory()
        self.request = self.factory.get("/")

        middleware = SessionMiddleware(lambda request: None)
        middleware.process_request(self.request)
        self.request.session.save()

        self.product1 = Product.objects.create(name="Product 1", slug="product-1", price=Decimal("10.00"), is_active=True)
        self.product2 = Product.objects.create(name="Product 2", slug="product-2", price=Decimal("20.00"), is_active=True)

    def test_get_cart_initializes_empty_cart(self):
        cart = get_cart(self.request)

        assert cart == {}
        assert CART_SESSION_KEY in self.request.session
        assert self.request.session["cart"] == {}
    
    def test_add_to_cart(self):
        add_to_cart(self.request, self.product1.id, quantity=2)
        cart = get_cart(self.request)

        assert str(self.product1.id) in cart
        assert cart[str(self.product1.id)]["quantity"] == 2
    
    def test_add_to_cart_increments_quantity(self):
        add_to_cart(self.request, self.product1.id, quantity=1)
        add_to_cart(self.request, self.product1.id, quantity=3)
        cart = get_cart(self.request)

        assert str(self.product1.id) in cart
        assert cart[str(self.product1.id)]["quantity"] == 4
    
    def test_update_cart_quantity(self):
        add_to_cart(self.request, self.product1.id, quantity=2)
        update_cart_quantity(self.request, self.product1.id, quantity=5)
        cart = get_cart(self.request)

        assert str(self.product1.id) in cart
        assert cart[str(self.product1.id)]["quantity"] == 5
    
    def test_update_cart_quantity_removes_when_zero(self):
        add_to_cart(self.request, self.product1.id, quantity=2)
        update_cart_quantity(self.request, self.product1.id, quantity=0)
        cart = get_cart(self.request)

        assert str(self.product1.id) not in cart
    
    def test_remove_from_cart(self):
        add_to_cart(self.request, self.product1.id, quantity=2)
        remove_from_cart(self.request, self.product1.id)
        cart = get_cart(self.request)

        assert str(self.product1.id) not in cart
    
    def test_get_cart_items(self):
        add_to_cart(self.request, self.product1.id, quantity=2)
        add_to_cart(self.request, self.product2.id, quantity=1)

        items = get_cart_items(self.request)

        assert len(items) == 2

        item1 = next(item for item in items if item["product"].id == self.product1.id)
        item2 = next(item for item in items if item["product"].id == self.product2.id)

        assert item1["quantity"] == 2
        assert item1["total_price"] == self.product1.price * 2

        assert item2["quantity"] == 1
        assert item2["total_price"] == self.product2.price * 1
    
    def test_cart_total_price(self):
        add_to_cart(self.request, self.product1.id, quantity=2)  # 2 * 10.00 = 20.00
        add_to_cart(self.request, self.product2.id, quantity=3)  # 3 * 20.00 = 60.00

        total = get_cart_total_price(self.request)

        assert total == Decimal("80.00")
    
    def test_cart_total_quantity(self):
        add_to_cart(self.request, self.product1.id, quantity=2)
        add_to_cart(self.request, self.product2.id, quantity=3)

        total_quantity = get_cart_total_quantity(self.request)

        assert total_quantity == 5