from products.models import Product
import logging

cart_logger = logging.getLogger("ecommerce.cart")
cart_service_logger = logging.getLogger("ecommerce.cart.services")

CART_SESSION_KEY = "cart"

def get_cart(request):
    """
    Returns the cart stored in session.
    Ensures cart always exists.
    """
    cart = request.session.get(CART_SESSION_KEY)

    if cart is None:
        cart = {}
        request.session[CART_SESSION_KEY] = cart

    return cart

def add_to_cart(request, product_id, quantity=1):
    cart = get_cart(request)
    product_id = str(product_id)

    if product_id in cart:
        cart[product_id]["quantity"] += quantity
        cart_service_logger.info("Cart item quantity updated", extra={"product_id": product_id, "quantity": cart[product_id]["quantity"]})

    else:
        cart[product_id] = {"quantity": quantity}
        cart_service_logger.info("Product added to cart", extra={"product_id": product_id, "quantity": quantity})

    request.session.modified = True

def remove_from_cart(request, product_id):
    cart = get_cart(request)
    product_id = str(product_id)

    if product_id in cart:
        del cart[product_id]
        cart_service_logger.info("Product removed from cart", extra={"product_id": product_id})
        request.session.modified = True

def update_cart_quantity(request, product_id, quantity):
    cart = get_cart(request)
    product_id = str(product_id)

    if product_id in cart:
        if quantity <= 0:
            del cart[product_id]
            cart_service_logger.info("Product removed from cart due to zero quantity", extra={"product_id": product_id})
        else:
            cart[product_id]["quantity"] = quantity
            cart_service_logger.info("Cart item quantity updated", extra={"product_id": product_id, "quantity": quantity})

        request.session.modified = True

def get_cart_items(request):
    """
    Returns cart items enriched with product objects.
    """
    cart = get_cart(request)
    product_ids = cart.keys()

    products = Product.objects.filter(id__in=product_ids, is_active=True)

    items = []

    for product in products:
        item = {
            "product": product,
            "quantity": cart[str(product.id)]["quantity"],
            "total_price": product.price * cart[str(product.id)]["quantity"],
        }
        items.append(item)

    return items

def get_cart_total_price(request):
    items = get_cart_items(request)
    return sum(item["total_price"] for item in items)


def get_cart_total_quantity(request):
    cart = get_cart(request)
    return sum(item["quantity"] for item in cart.values())
