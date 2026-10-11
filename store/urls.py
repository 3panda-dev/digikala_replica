from django.urls import path
from .views import *

urlpatterns = [
    path('all-stores/', StoreListView.as_view(), name='all-stores'),
    path('<int:pk>/products/', StoreProductsView.as_view(), name='store-products'),
    path('my-stores/', SellerStoreListView.as_view(), name='my-stores'),
    path('add-store/', SellerStoreCreateView.as_view(), name='add-store'),
    path('update-store/<int:pk>', SellerStoreUpdateView.as_view(), name='update-store'),
    path('store-detail/<int:pk>', SellerStoreDetailView.as_view(), name='store-detail'),
    path('delete-store/<int:pk>', SellerStoreDeleteView.as_view(), name='delete-store')
]
