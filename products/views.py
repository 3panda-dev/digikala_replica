from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from .models import Product, Category

def products(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    search = request.GET.get("search")
    sort = request.GET.get("sort", "newest")
    category = request.GET.get("category")

    if category:
        products = products.filter(category__name=category)

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
        "categories": categories,
    })

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    product.viewed()
    return render(request, "product_detail.html", {
        "product": product,
    })


