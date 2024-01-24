from captcha.fields import CaptchaField, CaptchaTextInput
from django import forms


class LoginForm(forms.Form):
    email = forms.CharField(
        widget=forms.EmailInput(attrs={'placeholder': 'Введите Вашу почту'}), label='')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль'}),
                               validators=['validate_password'], label='')


class RegisterForm(forms.Form):
    name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Контактное лицо'}), label='')
    phone = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Контактное лицо'}),
                            validators=['validate_phone'], label='')
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Введите Вашу почту'}), label='')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль'}),
                               validators=['validate_password'], label='')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Повторите пароль'}), label='')
    captcha = CaptchaField(
        label='',
        widget=CaptchaTextInput(attrs={'placeholder': 'Введите текст с картинки'}))


class EmailResetForm(forms.Form):
    email = forms.CharField(
        label='', widget=forms.EmailInput(attrs={'placeholder': 'Введите Вашу почту'}))
    captcha = CaptchaField(
        label='',
        widget=CaptchaTextInput(attrs={'placeholder': 'Введите текст с картинки'}))
