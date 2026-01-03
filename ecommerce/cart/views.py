from django.shortcuts import render, redirect, get_object_or_404
from cart.services import *

# Create your views here.

def cart_detail(request):
    cart_items = get_cart_items(request)
    total = get_cart_total_price(request)

    return render(request, "cart/cart.html", {
        "cart_items": cart_items,
          "total": total,
    })

def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)
    quantity = int(request.POST.get("quantity", 1))
    add_to_cart(request, product.id, quantity)

    return redirect("cart_detail")

def cart_update(request, product_id):
    quantity = int(request.POST.get("quantity", 1))
    update_cart_quantity(request, product_id, quantity)

    return redirect("cart_detail")

def cart_remove(request, product_id):
    remove_from_cart(request, product_id)
    return redirect("cart_detail")