from django import forms
from .models import *

class SellerProductCreateform(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['store', 'category', 'name', 'description', 'price', 'stock', 'image', 'status']

class SellerCategoryCreateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['store', 'name',]
        