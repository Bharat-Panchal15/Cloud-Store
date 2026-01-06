from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from orders.services import create_order_from_cart
from orders.models import Order
import logging

order_view_logger = logging.getLogger('ecommerce.orders.views')

# Create your views here.

@login_required
def order_list_view(request):
    """
    Display a list of orders for the logged-in user.
    """
    orders = Order.objects.filter(user=request.user).only('id', 'total_amount', 'status', 'created_at')
    order_view_logger.debug("Order list viewed", extra={"user_id": request.user.id, "orders_count": orders.count()})

    return render(request, 'orders/list.html', {'orders': orders})

@login_required
def order_detail_view(request, order_id):
    """
    Display details of a specific order.
    """
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_view_logger.debug("Order detail viewed", extra={"user_id": request.user.id, "order_id": order.id})
    items_list = order.items.select_related('product').all()

    items = []
    for item in items_list:
        items.append({
            'product': item.product,
            'quantity': item.quantity,
            'price_at_purchase': item.price_at_purchase,
            'subtotal': item.price_at_purchase * item.quantity,
        })

    return render(request, 'orders/detail.html', {'order': order, 'items': items})

@login_required
def order_confirmation_view(request, order_id):
    """
    Display order confirmation page after successful checkout.
    """
    order = get_object_or_404(Order, id=order_id, user=request.user)

    return render(request, 'orders/confirmation.html', {'order': order})

@login_required
@require_POST
def checkout_view(request):
    """
    Handle the checkout process by creating an order from the cart items.
    """
    
    try:
        order = create_order_from_cart(request, request.user)
    
    except ValueError:
        messages.error(request, "Your cart is empty. Please add items to your cart before checking out.")
        order_view_logger.warning("Checkout failed: empty cart", extra={"user_id": request.user.id})
        return redirect('cart_detail')
    order_view_logger.info("Checkout successful", extra={"user_id": request.user.id, "order_id": order.id})
    return redirect('order_confirmation', order_id=order.id)

