from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import UserRegisterForm, CustomAuthenticationForm


def login_view(request):  # Форма авторизации
    if request.method == 'POST':
        login_form = CustomAuthenticationForm(request, data=request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('pa')
    else:
        login_form = CustomAuthenticationForm()
    reg_form = UserRegisterForm()
    return render(request, 'main.html', {'login_form': login_form, 'reg_form': reg_form})


def registration(request):
    reg_form = UserRegisterForm(request.POST)
    if request.method == 'POST':
        if reg_form.is_valid():
            reg_form.save()
            return redirect('home')
    else:
        reg_form = UserRegisterForm()
    login_form = CustomAuthenticationForm()
    return render(request, 'main.html', {'reg_form': reg_form, 'login_form': login_form})


def logout_view(request):
    logout(request)
    return redirect('home')
