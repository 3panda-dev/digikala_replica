from django.urls import path
from .views import CheckoutView, order_history

urlpatterns = [
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('order_history/', order_history, name='order_history')
]
