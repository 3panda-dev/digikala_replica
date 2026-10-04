from django.shortcuts import render

from products.models import Product

def home(request):
    product = Product()
    return render(request, "home.html", {"most_viewed_product": product})