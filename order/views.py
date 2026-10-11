from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views import View

from order.models import Order

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


@login_required
def order_history(request):
    profile = request.user.customerprofile
    orders = Order.objects.filter(customer=profile).select_related('customer')
    return render(request, 'order_history.html', {'orders': orders})