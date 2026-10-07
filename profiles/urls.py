from django.urls import path
from .views import *

urlpatterns = [
    path('customer-profile/<int:pk>/', ProfileDetailView.as_view(), name='profile_detail')
]