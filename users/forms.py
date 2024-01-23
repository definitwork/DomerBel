from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from captcha.fields import CaptchaField
from .models import User
from django import forms
from django.contrib.auth.forms import UsernameField
from django.utils.translation import gettext_lazy as _


class CustomUserCreationForm(UserCreationForm):
    captcha = CaptchaField(label="Введите код с картинки")

    def __init__(self, *args, **kwargs):  # Переопределяем класс UserCreationForm
        super().__init__(*args, **kwargs)
        self.fields.pop('password2')  # Убираем поле подтверждения второго пароля
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
        fields = ['first_name', 'phone_number', 'email']


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'auth_field check_auth_field'
        self.fields['password'].widget.attrs['class'] = 'auth_field check_auth_field'



#Johan добавил
class MyCustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("email",)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ("email",)
