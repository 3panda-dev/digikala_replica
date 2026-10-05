from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import login,logout
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView

class UserRegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, f'{self.object.first_name} سلام')
        return response
    def form_invalid(self, form):
        messages.error(self.request, 'ثبت نام انجام نشد')
        return super().form_invalid(form)

class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'registration/login.html'
    next_page = reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.get_user()
        messages.success(self.request, f'{user.first_name} سلام')
        return response
    def form_invalid(self, form):
        messages.error(self.request, 'ورود انجام نشد')
        return super().form_invalid(form)

def User_logout_view(request):
    logout(request)
    messages.info(request, 'کاربر با موفقیت خارج شد')
    return redirect(reverse('home'))
