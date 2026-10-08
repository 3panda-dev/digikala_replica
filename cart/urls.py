from django.urls import path
from . import views

urlpatterns = [
    path('my_cart/', views.my_cart, name='my_cart'),
    path('add_to_cart/<int:product_id>/', views.AddToCart.as_view(), name='add_to_cart'),
]