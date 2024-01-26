from django.contrib.auth import logout, authenticate, login
from django.http import JsonResponse
from django.shortcuts import redirect

from .captcha import random_digit_challenge
from .forms import LoginForm, RegisterForm


def logout_view(request):
    logout(request)
    return redirect('home')


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({'success': True})  # Есть в базе
            elif user is None:
                return JsonResponse({'errors': 1})  # Неверный email или пароль
        else:
            return JsonResponse({'errors': 1})  # Неверный email или пароль


def register_view(request):
    if request.method == 'POST':
        print(request.POST)
        form = RegisterForm(request.POST)
        if form.is_valid():
            print(form.errors)
            # return JsonResponse({'success': True})
            return redirect('home')
        else:
            return JsonResponse({'errors': form.errors})
        return JsonResponse({'errors': 'aswdasd'})
