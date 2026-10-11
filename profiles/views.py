from decimal import Decimal
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, get_object_or_404
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, UpdateView


class ProfileDetailView(DetailView):
    model = CustomerProfile
    queryset = CustomerProfile.objects.select_related('user')
    template_name = 'customer_panel.html'
    context_object_name = 'profile_detail'


class IncreaseBalance(LoginRequiredMixin, UpdateView):
    model = CustomerProfile
    fields = ['wallet']
    template_name = 'increase_balance.html'
    context_object_name = 'profile'


    def get_object(self, queryset=None):
        return get_object_or_404(
            CustomerProfile,
            pk=self.kwargs['pk']
        )

    def form_valid(self, form):
        amount = form.cleaned_data['wallet']
        profile = form.instance

        profile.wallet += amount

        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'profile_detail',
            kwargs={'pk': self.object.pk}
        )