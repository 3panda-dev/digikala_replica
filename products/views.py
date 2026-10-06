from django.shortcuts import render
from django.views.generic import ListView
from .models import Product

def products(request):
    products = Product.objects.all()

    search = request.GET.get("search")
    sort = request.GET.get("sort", "newest")

    if search:
        products = products.filter(name__icontains=search)

    if sort == "newest":
        products = products.order_by("-created_at")

    elif sort == "oldest":
        products = products.order_by("created_at")

    elif sort == "most_viewed":
        products = products.order_by("-views_count")

    return render(request, "products.html", {
        "products": products,
    })

def product_detail(request, slug):
    product = Product.objects.get(slug=slug)
    product.viewed()
    return render(request, "product_detail.html", {
        "product": product,
    })


# Create your views here.
