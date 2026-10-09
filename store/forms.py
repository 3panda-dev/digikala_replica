from django import forms
from .models import *

class SellerAddStoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['name', 'description']