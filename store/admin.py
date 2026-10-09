from .models import Store
from django.contrib import admin

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'seller', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'seller')
    list_editable = ('is_active',)
