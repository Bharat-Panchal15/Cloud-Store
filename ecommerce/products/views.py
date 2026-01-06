from django.shortcuts import render, get_object_or_404
from django.http import Http404
from products.models import Product
import logging

home_logger = logging.getLogger('ecommerce.products.home')
detail_logger = logging.getLogger('ecommerce.products.detail')

# Create your views here.

def home_view(request):
    products = Product.objects.filter(is_active=True)

    if not products.exists():
        home_logger.info("Home page loaded with no active products.")

    return render(request, 'products/home.html', {'products': products})

def product_detail_view(request, slug):
    try:
        product = Product.objects.get(slug=slug)
    except Product.DoesNotExist:
        detail_logger.debug("Product detail requested for non-existent slug", extra={'slug': slug})
        raise Http404()
    
    if not product.is_active:
        detail_logger.debug("Inactive product access attempt", extra={'product_id': product.id, 'slug': slug})
        raise Http404()
    return render(request, 'products/product.html', {'product': product})