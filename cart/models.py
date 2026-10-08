from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib import messages

class Cart(models.Model):
    profile = models.OneToOneField("profiles.CustomerProfile",  on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated at"))
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name=_("total"))

    def __str__(self):
        return f"Cart {self.id} for {self.profile.full_name}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE, name="product")
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Cart {self.cart.id}"

    def add_item(self):
        if self.product.stock <= self.quantity:
            raise ValueError("Cannot add more items than available in stock.")
        else:
            self.quantity += 1
            self.save()

    def remove_quantity(self):
        if self.quantity > 1:
            self.quantity -= 1
            self.save()
        else:
            self.delete()

    @property
    def get_total_price(self):
        return self.product.price * self.quantity