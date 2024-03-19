from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth.hashers import check_password
from django_recaptcha.fields import ReCaptchaField

from .models import User
from .validators import validate_password, validate_email, validate_phone


class LoginForm(forms.Form):
    email = forms.CharField(
        widget=forms.EmailInput(attrs={'id': 'email_login_field', 'placeholder': 'Введите Вашу почту'}),
        label='', validators=[validate_email])
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'id': 'password_login_field', 'placeholder': 'Введите пароль'}), label='')


class RegisterForm(forms.Form):
    name = forms.CharField(error_messages={'required': 'Не указано контактное лицо'},
                           max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Контактное лицо'}), label='')
    phone = forms.CharField(error_messages={'required': 'Не указан номер телефона'},
                            widget=forms.TextInput(attrs={'placeholder': 'Номер телефона'}),
                            validators=[validate_phone], label='')
    email = forms.CharField(error_messages={'required': 'Не указан email'},
                            widget=forms.EmailInput(
                                attrs={'id': 'email_register_field', 'placeholder': 'Введите Вашу почту'}),
                            validators=[validate_email], label='')
    password = forms.CharField(error_messages={'required': 'Введите пароль'},
                               widget=forms.PasswordInput(
                                   attrs={'placeholder': 'Введите пароль'}),
                               validators=[validate_password], label='')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Повторите пароль'}), label='')
    captcha = ReCaptchaField(label='')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        if password and password2 and password != password2:
            self.add_error('password2', 'Пароли не совпадают')


class EmailResetForm(forms.Form):
    email = forms.CharField(
        label='', widget=forms.EmailInput(attrs={'id': 'email_reset_field', 'placeholder': 'Введите Вашу почту'}))
    captcha = ReCaptchaField(label='')


class EditContactDataForm(forms.ModelForm):
    first_name = forms.CharField(required=True, error_messages={'required': 'Не указано контактное лицо'},
                                 widget=forms.TextInput(attrs={'class': 'input_field'}),
                                 label='Контактное лицо')
    phone_number = forms.CharField(required=True, error_messages={'required': 'Не указан номер телефона'},
                                   widget=forms.TextInput(attrs={'class': 'input_field'}),
                                   validators=[validate_phone],
                                   label='Телефон')
    email = forms.EmailField(required=True, error_messages={'required': 'Не указан email'},
                             widget=forms.TextInput(attrs={'class': 'input_field'}),
                             validators=[validate_email],
                             label='E-MAIL')

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'email', 'phone_number']


class ChangePasswordForm(forms.ModelForm):
    password = forms.CharField(error_messages={'required': 'Введите старый пароль'},
                               label='Введите старый пароль',
                               widget=forms.PasswordInput(
                                   attrs={'class': 'input_field', 'placeholder': 'Введите старый пароль'}),
                               validators=[validate_password])
    new_password = forms.CharField(error_messages={'required': 'Введите новый пароль'}, widget=forms.PasswordInput(
        attrs={'class': 'input_field', 'placeholder': 'Введите новый пароль'}),
                                   validators=[validate_password], label='Введите новый пароль')
    repeat_new_pass = forms.CharField(error_messages={'required': 'Повторите новый пароль'}, widget=forms.PasswordInput(
        attrs={'class': 'input_field', 'placeholder': 'Повторите новый пароль'}),
                                      validators=[validate_password], label='Повторите новый пароль')

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        repeat_new_pass = cleaned_data.get('repeat_new_pass')
        if new_password is not None and repeat_new_pass is not None and new_password != repeat_new_pass:
            self.add_error('repeat_new_pass', 'Пароли не совпадают')

    class Meta:
        model = get_user_model()
        fields = ['password']


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'auth_field check_auth_field'
        self.fields['password'].widget.attrs['class'] = 'auth_field check_auth_field'


# Johan добавил
class MyCustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email",)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("email",)
