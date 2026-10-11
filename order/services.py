from django.db import transaction
from .models import *

def create_order(customer, items):
    with transaction.atomic():
        order = Order.objects.create(customer=customer, total_amount=0)
        total_amount = 0

        for item in items:
            product = item.product
            quantity = item.quantity
            price = product.price * quantity
            OrderItem.objects.create(order=order, product=product, quantity=quantity, price=price)
            total_amount += price

        order.total_amount = total_amount
        order.save()

    pass