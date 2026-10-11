from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import View

from .services import create_order


class CheckoutView(LoginRequiredMixin, View):
    def post(self, request):
        try:
            create_order(request.user.customerprofile)
        except ValueError as error:
            messages.error(request, str(error))
            return redirect('my_cart')

        messages.success(request, 'Your order has been placed successfully.')
        return redirect('my_cart')
