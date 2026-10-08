from django.urls import path
from . import views

urlpatterns = [
    path('my_cart/', views.my_cart, name='my_cart'),
    path('cart/add_to_cart/<int:product_id>/', views.AddToCart.as_view(), name='add_to_cart'),
    path('cart/remove_from_cart/<int:product_id>/', views.RemoveFromCart.as_view(), name='remove_from_cart'),
    path('cart/add_quantity/<int:product_id>/', views.AddQuantity.as_view(), name='add_quantity'),
    path('cart/remove_quantity/<int:product_id>/', views.RemoveQuantity.as_view(), name='remove_quantity'),
]