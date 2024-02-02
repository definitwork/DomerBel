from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordResetView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import UserRegisterForm, CustomAuthenticationForm, SendEmailForm


def login_view(request):  # Форма авторизации
    if request.method == 'POST':
        login_form = CustomAuthenticationForm(request, data=request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('personal_account')
    else:
        login_form = CustomAuthenticationForm()
    email_form = SendEmailForm()
    reg_form = UserRegisterForm()
    return render(request, 'main.html', {'login_form': login_form, 'reg_form': reg_form, 'email_form': email_form})


def registration(request):
    reg_form = UserRegisterForm(request.POST)
    if request.method == 'POST':
        if reg_form.is_valid():
            reg_form.save()
            return redirect('home')
    else:
        reg_form = UserRegisterForm()
    email_form = SendEmailForm()
    login_form = CustomAuthenticationForm()
    return render(request, 'main.html', {'reg_form': reg_form, 'login_form': login_form, 'email_form': email_form})


def send_email(request):  # Функция для проверки капчи
    if request.method == "POST":
        email_form = SendEmailForm(request.POST)
        if email_form.is_valid():
            email = email_form.cleaned_data.get('email')
            # Нужно этот имейл перебросить в pasword reset
            # return email
    else:
        email_form = SendEmailForm()
    login_form = CustomAuthenticationForm()
    reg_form = UserRegisterForm()
    return render(request, 'main.html', {'email_form': email_form, 'reg_form': reg_form, 'login_form': login_form})


class CustomPasswordResetView(PasswordResetView):
    email_template_name = 'users/password_reset_email.html'
    success_url = reverse_lazy('users:password_reset_done')
    # form_class = 'forget_pass_form'
    # from_email = send_email(request)



def logout_view(request):
    logout(request)
    return redirect('home')
