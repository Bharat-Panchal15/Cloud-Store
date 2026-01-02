from django.shortcuts import render
from products.models import Product

# Create your views here.

def home_view(request):
    products = Product.objects.filter(is_active=True)
    return render(request, 'products/home.html', {'products': products})