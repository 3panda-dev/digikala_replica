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



# Create your views here.
