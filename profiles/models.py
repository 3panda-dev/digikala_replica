
from django.db import models 
from django.conf import settings 
from django.utils.translation import gettext_lazy as _ 
from django.db.models.signals import post_save 
from django.dispatch import receiver 

from cart.models import Cart
 
class CustomerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=300, verbose_name='نام کامل')
    location = models.CharField(max_length=1000, blank=True, null=True, verbose_name='آدرس')
    postal_code = models.CharField(max_length=10, blank=True, null=True, verbose_name='کد پستی')
    avatar = models.ImageField(upload_to='profile-customer-avatars/', blank=True, null=True, verbose_name='عکس پروفایل')
    wallet = models.DecimalField(max_digits=12, decimal_places=0,default=0, verbose_name='کیف پول')

    
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True) 
 
    class Meta: 
        verbose_name = 'پروفایل مشتری' 
        verbose_name_plural = 'پروفایل مشتریان' 
        ordering = ('-created_at',) 
 
    def __str__(self): 
        return self.full_name 
 
class sellerprofile(models.Model): 
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    national_id = models.CharField(max_length=10, unique=True, verbose_name='کد ملی') 
    shaba_number = models.CharField(max_length=26, blank=True, null=True, verbose_name='شماره شبا') 
    avatar = models.ImageField(upload_to='profile-seller-avatars/', blank=True, null=True, verbose_name='عکس پروفایل') 
 
 
 
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True) 
 
    class Meta: 
        verbose_name = 'پروفایل فروشنده' 
        verbose_name_plural = 'پروفایل فروشندگان' 
        ordering = ('-created_at',) 
 
    def __str__(self): 
        return self.national_id 
 
 
@receiver(post_save, sender=settings.AUTH_USER_MODEL) 
def manage_profile(sender, instance, created, **kwargs): 
    full_name = f"{instance.first_name} {instance.last_name}".strip() 
    if created: 
        profile = CustomerProfile.objects.create(user=instance, full_name=full_name)
        Cart.objects.create(profile=profile)
    else: 
        CustomerProfile.objects.update_or_create(user=instance, defaults={'full_name':full_name})
