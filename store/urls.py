from django.urls import path
from .views import *

urlpatterns = [
    path('my-stores/', SellerStoreListView.as_view(), name='my-stores'),
    path('add-store/', SellerStoreCreateView.as_view(), name='add-store'),
    path('update-store/<int:pk>', SellerStoreUpdateView.as_view(), name='update-store'),
    path('store-detail/<int:pk>', SellerStoreDetailView.as_view(), name='store-detail')
]
