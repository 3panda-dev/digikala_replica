from django.shortcuts import render
from .models import *
from django.views.generic import DetailView

class ProfileDetailView(DetailView):
    model = CustomerProfile
    queryset = CustomerProfile.objects.select_related('user')
    template_name = 'customer_panel.html'
    context_object_name = 'profile_detail'