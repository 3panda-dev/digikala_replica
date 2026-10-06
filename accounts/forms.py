from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import *

class UserRegisterForm(UserCreationForm):
    phone_number = forms.CharField(max_length=11, label='تلفن')

    class Meta:
        model = User
        fields = ['phone', 'first_name', 'last_name',]

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=11,)
    password = forms.CharField(max_length=150,)