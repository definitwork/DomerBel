from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy

from .models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm


def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse('Вы успешно вошли в систему!')
        else:
            return HttpResponse('Неверный логин или пароль.')
    return render(request, 'registration/login.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['contact']
        email = request.POST['email']
        password = request.POST['password']
        repeat_password = request.POST['repeat_password']
        user = User(first_name=username, email=email, password=password)
        user.set_password()


# def reset_password(request):
#     if request.method == 'POST':
#         email = request.POST['email']
#         if User.objects.filter(email=email).exists():
#             return render(request, 'users/password_reset_form.html')
#
#         else:
#             print('нет такого')
#             return render(request, 'main.html', {'error': "Такого имейла нет"})


# def change_password(email, new_password):
#     user = User.objects.get(email=email)
#     user.set_password(new_password)
#     user.save()
# change_password('user@mail.ru', 'Ishimura2')


@login_required
def profile(request):
    return render(request, template_name='personal_account.html')
