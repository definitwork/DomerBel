from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render

from users.forms import UserRegisterForm, CustomAuthenticationForm


# Create your views here.

# Использую на главной вьюшке 2 формы связанные с юзером
# для того что бы при вызове главной страницы они отрендерелись в pop-up окнах
def get_main_page(request):
    reg_form = UserRegisterForm()
    login_form = CustomAuthenticationForm()
    return render(request, 'main.html', {'reg_form': reg_form, 'login_form': login_form})


def get_help_page(request):
    return render(request, 'help.html')


def get_personal_account_page(request):
    return render(request, 'personal_account.html')


def get_user_data_page(request):
    return render(request, 'user_data.html')


def get_incoming_page(request):
    return render(request, 'incoming_messages.html')


def get_outgiong_page(request):
    return render(request, 'outgiong_messages.html')


def get_sent_page(request):
    return render(request, 'sent_messages.html')


def get_admin_message_page(request):
    return render(request, 'admin_message.html')
