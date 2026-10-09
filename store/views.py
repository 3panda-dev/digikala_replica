from django.shortcuts import render
from .models import *
from .forms import *
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse, reverse_lazy


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
    template_name = 'store_detail.html'
    context_object_name = 'store_detail_view'

    def test_func(self):
        return self.request.user.is_seller
    def get_queryset(self):
        return Store.objects.filter(seller=self.request.user.sellerprofile)

