from django.shortcuts import render, get_object_or_404
from .models import *
from .forms import *
from products.models import Product
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse, reverse_lazy


class StoreListView(ListView):
    model = Store
    template_name = 'all_stores.html'
    context_object_name = 'stores'

    def get_queryset(self):
        return Store.objects.filter(is_active=True).order_by('name')


class StoreProductsView(ListView):
    model = Product
    template_name = 'store_detail.html'
    context_object_name = 'products'

    def get_store(self):
        if not hasattr(self, 'store'):
            self.store = get_object_or_404(Store, pk=self.kwargs['pk'], is_active=True)
        return self.store

    def get_queryset(self):
        queryset = Product.objects.filter(
            store=self.get_store(),
            is_active=True,
            status=Product.Status.PUBLISHED,
        ).prefetch_related('category')

        search = self.request.GET.get('search', '').strip()
        sort = self.request.GET.get('sort', 'newest')

        if search:
            queryset = queryset.filter(name__icontains=search)

        if sort == 'oldest':
            queryset = queryset.order_by('created_at')
        elif sort == 'most_viewed':
            queryset = queryset.order_by('-views_count', '-created_at')
        elif sort == 'price_low':
            queryset = queryset.order_by('price', 'name')
        elif sort == 'price_high':
            queryset = queryset.order_by('-price', 'name')
        else:
            queryset = queryset.order_by('-created_at')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['store'] = self.get_store()
        return context


class SellerStoreListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Store
    template_name = 'stores.html'
    context_object_name = 'stores'

    def test_func(self):
        return self.request.user.is_seller

    def get_queryset(self):
        return Store.objects.filter(seller=self.request.user.sellerprofile)


class SellerStoreCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    form_class = SellerAddStoreForm
    template_name = 'create_store.html'
    success_url = reverse_lazy('my-stores')

    def test_func(self):
        return self.request.user.is_seller

    def form_valid(self, form):
        form.instance.seller = self.request.user.sellerprofile
        return super().form_valid(form)


class SellerStoreUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Store
    form_class = SellerAddStoreForm
    template_name = 'create_store.html'
    success_url = reverse_lazy('my-stores')

    def test_func(self):
        return self.request.user.is_seller

    def get_queryset(self):
        return Store.objects.filter(seller=self.request.user.sellerprofile)


class SellerStoreDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Store
    template_name = 'seller_store_detail.html'
    context_object_name = 'store_detail_view'

    def test_func(self):
        return self.request.user.is_seller

    def get_queryset(self):
        return Store.objects.filter(seller=self.request.user.sellerprofile)


class SellerStoreDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Store
    template_name = 'delete_store.html'
    success_url = reverse_lazy('my-stores')

    def test_func(self):
        return self.request.user.is_seller

    def get_queryset(self):
        return Store.objects.filter(seller=self.request.user.sellerprofile)
