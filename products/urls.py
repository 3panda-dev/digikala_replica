from django.urls import path
from .views import *

urlpatterns = [
    path('products/', products, name='products'),
    path('product/<str:slug>/', product_detail, name='product_detail'),
    path('seller-product-list/', SellerProductListView.as_view(), name='seller-product-list'),
    path('add-product/', SellerProductCreateView.as_view(), name='seller-add-product'),
    path('update-product/<int:pk>', SellerProductUpdateView.as_view(), name='seller-update-product'),
    path('delete-product/<int:pk>', SellerProductDeleteView.as_view(), name='delete-product'),
    path('seller-category-list/', SellerCategoryListView.as_view(), name='seller-category-list'),
    path('seller-add-category/', SellerCategoryCreateView.as_view(), name='seller-add-category'),
    path('delete-category/<int:pk>', SellerCategoryDeleteView.as_view(), name='delete-category')
]
