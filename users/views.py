from django.contrib.auth import logout, authenticate, login, get_user_model
from django.http import JsonResponse
from django.shortcuts import redirect
from .forms import LoginForm, RegisterForm
from .models import User


def logout_view(request):
    logout(request)
    return redirect('home')


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'errors': 1})
        else:
            return JsonResponse({'errors': 1})


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User()
            user.first_name = form.cleaned_data.get('name')
            user.phone_number = form.cleaned_data.get('phone')
            user.email = form.cleaned_data.get('email')
            user.set_password(form.cleaned_data.get('password'))
            user.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'errors': form.errors})


