from django.shortcuts import render
from products.models import Product

def home(request):
    product = Product.objects.filter(status="published")
    return render(request, "home.html", {"products": product})