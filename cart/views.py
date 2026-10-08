from django.shortcuts import render
from .models import Cart, CartItem
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from products.models import Product
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import get_object_or_404, redirect


@login_required
def my_cart(request):
    cart = Cart.objects.get(profile=request.user.customerprofile)
    return render(request, 'my_cart.html', {'cart': cart})



class AddToCart(LoginRequiredMixin, View):

    def post(self,request, product_id):
        product = get_object_or_404(Product, id=product_id)
        cart = Cart.objects.get(profile=request.user.customerprofile)

        if cart.items.filter(product=product).exists():
            messages.info(request, "Product already in cart.")

        elif cart.items.filter(product=product).exists():
            try:
                CartItem.objects.create(cart=cart, product=product, quantity=1)
                messages.success(request, "Quantity added successfully.")
            except ValueError as e:
                messages.error(request, str(e))
        else:
            messages.success(request, "Product added to cart.")

        return redirect('my_cart')