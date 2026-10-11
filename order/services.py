from decimal import Decimal

from django.db import transaction

from cart.models import Cart
from profiles.models import CustomerProfile
from products.models import Product
from .models import Order, OrderItem


def create_order(customer):
    """Create an order and move wallet balances as one database transaction."""
    with transaction.atomic():
        cart = Cart.objects.select_for_update().get(profile=customer)
        cart_items = list(cart.items.all())

        if not cart_items:
            raise ValueError('Your cart is empty.')

        product_ids = [item.product_id for item in cart_items]
        locked_products = Product.objects.select_for_update().filter(
            pk__in=product_ids
        ).select_related('store__seller')
        products = {product.pk: product for product in locked_products}

        if len(products) != len(set(product_ids)):
            raise ValueError('A product in your cart no longer exists.')

        total = Decimal('0')
        seller_totals = {}
        order_lines = []

        for item in cart_items:
            product = products[item.product_id]

            if not product.is_active or product.status != Product.Status.PUBLISHED or not product.store.is_active:
                raise ValueError(f'{product.name} is no longer available.')

            if item.quantity < 1 or product.stock < item.quantity:
                raise ValueError(f'Not enough stock for {product.name}.')

            line_total = Decimal(product.price) * item.quantity
            total += line_total
            seller_user_id = product.store.seller.user_id
            seller_totals[seller_user_id] = seller_totals.get(seller_user_id, Decimal('0')) + line_total
            order_lines.append((product, item.quantity, Decimal(product.price)))

        if total <= 0:
            raise ValueError('Invalid order total.')

        # Every seller also has a CustomerProfile in this project; their wallet is stored there.
        profile_user_ids = sorted(set(seller_totals) | {customer.user_id})
        locked_profiles = CustomerProfile.objects.select_for_update().filter(
            user_id__in=profile_user_ids
        ).order_by('pk')
        profiles_by_user = {profile.user_id: profile for profile in locked_profiles}

        buyer = profiles_by_user.get(customer.user_id)
        if buyer is None:
            raise ValueError('Your customer profile could not be found.')

        for seller_user_id in seller_totals:
            if seller_user_id not in profiles_by_user:
                raise ValueError('A seller wallet could not be found.')

        if buyer.wallet < total:
            raise ValueError('Insufficient balance in wallet.')

        order = Order.objects.create(customer=buyer, total_amount=total)

        buyer.wallet -= total
        buyer.save(update_fields=['wallet'])

        for seller_user_id, amount in seller_totals.items():
            seller_profile = profiles_by_user[seller_user_id]
            seller_profile.wallet += amount
            seller_profile.save(update_fields=['wallet'])

        for product, quantity, price in order_lines:
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=price,
            )
            product.stock -= quantity
            product.save(update_fields=['stock'])

        cart.items.all().delete()

    return order
