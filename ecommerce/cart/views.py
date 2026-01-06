from django.shortcuts import render, redirect, get_object_or_404
from cart.services import *
import logging

cart_logger = logging.getLogger("ecommerce.cart.views")

# Create your views here.

def cart_detail(request):
    cart_items = get_cart_items(request)
    total = get_cart_total_price(request)

    if not cart_items:
        cart_logger.debug("Cart page accessed with empty cart")

    return render(request, "cart/cart.html", {
        "cart_items": cart_items,
          "total": total,
    })

def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)
    quantity = int(request.POST.get("quantity", 1))
    add_to_cart(request, product.id, quantity)

    cart_logger.info("Product added to cart via view", extra={"product_id": product.id, "quantity": quantity})

    return redirect("cart_detail")

def cart_update(request, product_id):
    quantity = int(request.POST.get("quantity", 1))
    update_cart_quantity(request, product_id, quantity)

    cart_logger.info("Cart item quantity updated via view", extra={"product_id": product_id, "quantity": quantity})

    return redirect("cart_detail")

def cart_remove(request, product_id):
    remove_from_cart(request, product_id)
    cart_logger.info("Cart item removed via view", extra={"product_id": product_id})
    return redirect("cart_detail")