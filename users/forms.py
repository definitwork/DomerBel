from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from captcha.fields import CaptchaField
from .validators import validate_phone

from .models import User
from django import forms
from django.contrib.auth.forms import UsernameField
from django.utils.translation import gettext_lazy as _


class SendEmailForm(forms.Form):
    email = forms.EmailField()
    captcha = CaptchaField(label="Введите код с картинки")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['class'] = 'send_email_field'

    class Meta:
        model = get_user_model()
        fields = ['email']


class CustomUserCreationForm(UserCreationForm):
    captcha = CaptchaField(label="Введите код с картинки")
    phone_number = forms.CharField(validators=[validate_phone])

    def __init__(self, *args, **kwargs):  # Переопределяем класс UserCreationForm
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = ''  # Избавляемся он текста подсказки каким должен быть пароль
        # классы для полей регистрации
        # Первый что-бы дергать по JS , второй для стилизации
        self.fields['email'].widget.attrs['class'] = 'check_register_field check_auth_field'
        self.fields['phone_number'].widget.attrs['class'] = 'check_register_field check_auth_field'
        self.fields['first_name'].widget.attrs['class'] = 'check_register_field check_auth_field'
        self.fields['password1'].widget.attrs['class'] = 'check_register_field check_auth_field'


class UserRegisterForm(CustomUserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'email', 'phone_number', 'password1']


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'auth_field check_auth_field'
        self.fields['password'].widget.attrs['class'] = 'auth_field check_auth_field'
