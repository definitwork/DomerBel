from django import forms
from django.contrib.auth import get_user_model
from django_recaptcha.fields import ReCaptchaField

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
    phone = forms.CharField(error_messages={'required': 'Не указан телефон'},
                            widget=forms.TextInput(attrs={'placeholder': 'Номер телефона'}),
                            validators=[validate_phone], label='')
    email = forms.CharField(error_messages={'required': 'Не указан email'},
                            widget=forms.EmailInput(
                                attrs={'id': 'email_register_field', 'placeholder': 'Введите Вашу почту'}),
                            validators=[validate_email], label='')
    password = forms.CharField(error_messages={'required': 'Введите пароль'},
                               widget=forms.PasswordInput(
                                   attrs={'id': 'password_register_field', 'placeholder': 'Введите пароль'}),
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


# validators=[validate_password], label='Пароль',
#                                    required=False)
class EditProfileForm(forms.ModelForm):
    first_name = forms.CharField(label='Контактное лицо', required=False)
    phone_number = forms.CharField(validators=[validate_phone], label='Телефон', required=False)
    email = forms.EmailField(validators=[validate_email], label='E-MAIL', required=False)

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'phone_number', 'email']


class PasswordResetPersonForm(forms.ModelForm):
    password = forms.CharField(error_messages={'required': 'Введите пароль'}, label='',
                               widget=forms.PasswordInput(
                                   attrs={'id': 'password_person_reset_field', 'placeholder': 'Введите старый пароль'}))

    class Meta:
        model = get_user_model()
        fields = ['password']
