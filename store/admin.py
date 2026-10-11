from .models import *
from django.contrib import admin

@admin.register(BusinessType)
class BusinessTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'seller', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'seller')
    list_editable = ('is_active',)
