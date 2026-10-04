from django.shortcuts import render
from django.views.generic import ListView


from .models import Product


class ProductList(ListView):
    template_name = "product.html"
    queryset = Product.objects.all()
    context_object_name = "Product"

# Create your views here.
