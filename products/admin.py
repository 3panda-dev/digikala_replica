from django.contrib import admin
from .models import *

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)
    list_editable = ('is_active',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'views_count', 'status')
    list_filter = ('category', 'status')
    readonly_fields = ('views_count',)
    search_fields = ('category', 'name', 'description')
    list_editable = ('price', 'status')
    fieldsets = (
        ('INFO', {
            'fields':('name', 'category', 'description', 'views_count', 'slug', 'status')
        }),
        ('PRICE & STOCK', {
            'fields': ('price', 'stock')
        }),
        ('product image', {
            'fields': ('image',)
        }),
    )


