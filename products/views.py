from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import *
from .forms import *
from django.urls import reverse, reverse_lazy
from django.utils.text import slugify


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


class SellerProductListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Product
    template_name = 'seller_product_list.html'
    context_object_name = 'seller_product_list'

    def test_func(self):
        return self.request.user.is_seller
    def get_queryset(self):
        queryset = Product.objects.filter(store__seller=self.request.user.sellerprofile)
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)
        return queryset

class SellerProductCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView): 
    form_class = SellerProductCreateform
    template_name = 'create_product.html'
    success_url = reverse_lazy('seller-product-list')

    def test_func(self):
        return self.request.user.is_seller
    
    def form_valid(self, form):
        product = form.save(commit=False)
        if not product.slug:
            product.slug = slugify(product.name, allow_unicode=True)

        product.save()
        form.save_m2m()

        return super().form_valid(form)
    
    def get_form(self, form_class = None):
        form = super().get_form(form_class)
        form.fields['store'].queryset = self.request.user.sellerprofile.stores.all()
        form.fields['category'].queryset = Category.objects.filter(store__seller=self.request.user.sellerprofile)
        return form

class SellerProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = SellerProductCreateform
    template_name = 'create_product.html'
    success_url = reverse_lazy('seller-product-list')

    def test_func(self):
        return self.request.user.is_seller
    def get_queryset(self):
        return Product.objects.filter(store__seller=self.request.user.sellerprofile).distinct()
    def get_form(self, form_class = None):
            form = super().get_form(form_class)
            form.fields['category'].queryset = Category.objects.filter(store__seller=self.request.user.sellerprofile)
            return form

class SellerProductDeleteView(LoginRequiredMixin, UserPassesTestMixin,DeleteView):
    model = Product
    template_name = 'delete_product.html'
    success_url = reverse_lazy('seller-product-list')

    def test_func(self):
        return self.request.user.is_seller
    def get_queryset(self):
        return Product.objects.filter(store__seller=self.request.user.sellerprofile).distinct()

class SellerCategoryListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Category
    template_name = 'category_list.html'
    context_object_name = 'seller_category_list'

    def test_func(self):
        return self.request.user.is_seller
    def get_queryset(self):
        return Category.objects.filter(store__seller=self.request.user.sellerprofile).distinct()

class SellerCategoryCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    form_class = SellerCategoryCreateForm
    template_name = 'create_category.html'
    success_url = reverse_lazy('seller-category-list')

    def test_func(self):
        return self.request.user.is_seller
    
    def form_valid(self, form):
        category = form.save(commit=False)

        if not category.slug:
            category.slug = slugify(category.name, allow_unicode=True)

        category.save()
        self.object = category
        return redirect(self.get_success_url())

    def get_form(self, form_class = None):
        form = super().get_form(form_class)
        form.fields['store'].queryset = self.request.user.sellerprofile.stores.all()
        return form

class SellerCategoryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Category
    template_name = 'delete_category.html'
    success_url = reverse_lazy('seller-category-list')

    def test_func(self):
        return self.request.user.is_seller
    def get_queryset(self):
        return Category.objects.filter(store__seller=self.request.user.sellerprofile).distinct()