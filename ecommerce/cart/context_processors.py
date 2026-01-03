from cart.services import get_cart_total_quantity

def cart_context(request):
    """
    Context processor to add cart total quantity to the context.
    """
    return {
        'cart_total_quantity': get_cart_total_quantity(request)
    }