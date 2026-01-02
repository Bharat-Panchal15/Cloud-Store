from django.shortcuts import render, get_object_or_404
from products.models import Product

# Create your views here.

def home_view(request):
    products = Product.objects.filter(is_active=True)
    return render(request, 'products/home.html', {'products': products})

def product_detail_view(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)

    return render(request, 'products/product.html', {'product': product})