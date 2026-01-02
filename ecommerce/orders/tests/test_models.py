import pytest
from django.contrib.auth import get_user_model
from orders.models import Order, OrderItem
from products.models import Product
from decimal import Decimal

User = get_user_model()

@pytest.mark.django_db
class TestOrderModel:
    def setup_method(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpassword123",
        )
        self.product = Product.objects.create(
            name="Test Product",
            slug="test-product",
            price=Decimal("49.99")
        )
    
    def test_create_order(self):
        order = Order.objects.create(
            user=self.user,
            total_amount=Decimal("49.99"),
            status="PENDING"
        )

        assert order.user == self.user
        assert order.total_amount == Decimal("49.99")
        assert order.status == "PENDING"
        assert order.created_at is not None
        assert str(order).startswith("Order")
    
    def test_create_order_item(self):
        order = Order.objects.create(
            user=self.user,
            total_amount=Decimal("49.99"),
            status="PENDING"
        )
        order_item = OrderItem.objects.create(
            order=order,
            product=self.product,
            quantity=2,
            price_at_purchase=Decimal("49.99")
        )

        assert order_item.order == order
        assert order_item.product == self.product
        assert order_item.quantity == 2
        assert order_item.price_at_purchase == Decimal("49.99")
        assert str(order_item) == f"2 x {self.product} for Order #{order.id}"
    
    def test_order_related_name_items(self):
        order = Order.objects.create(
            user=self.user,
            total_amount=Decimal("149.97")
        )
        OrderItem.objects.create(order=order,product=self.product,quantity=1,price_at_purchase=self.product.price)
        OrderItem.objects.create(order=order,product=self.product,quantity=3,price_at_purchase=self.product.price)

        items = order.items.all()
        quantities = [item.quantity for item in items]
        
        assert len(items) == 2
        assert quantities == [1,3]