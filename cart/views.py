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
    total = 0
    for item in cart.items.all():
        total += item.product.price * item.quantity
    return render(request, 'my_cart.html', {'cart': cart, "cart_total": total})



class AddToCart(LoginRequiredMixin, View):

    def post(self,request, product_id):
        product = get_object_or_404(Product, id=product_id)
        cart = Cart.objects.get(profile=request.user.customerprofile)

        if cart.items.filter(product=product).exists():
            messages.info(request, "Product already in cart.")

        else:

            try:
                CartItem.objects.create(cart=cart, product=product)
                messages.success(request, "product added successfully.")

            except ValueError as e:
                messages.error(request, str(e))

        return redirect('my_cart')


class RemoveFromCart(LoginRequiredMixin, View):

    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        cart = Cart.objects.get(profile=request.user.customerprofile)

        if cart.items.filter(product=product).exists():
            cart_item = cart.items.get(product=product)
            cart_item.delete()
            messages.success(request, "Product removed from cart.")
        else:
            messages.error(request, "Product not found in cart.")

        return redirect('my_cart')


class AddQuantity(LoginRequiredMixin, View):

    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        cart = Cart.objects.get(profile=request.user.customerprofile)
        cart_item = cart.items.get(product=product)

        try:
            cart_item.add_item()
            messages.success(request, "Quantity increased successfully.")
            
        except ValueError as e:
            messages.error(request, str(e))

        return redirect('my_cart')

class RemoveQuantity(LoginRequiredMixin, View):

    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        cart = Cart.objects.get(profile=request.user.customerprofile)
        cart_item = cart.items.get(product=product)
        cart_item.remove_quantity()

        return redirect('my_cart')

