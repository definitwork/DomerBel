from django import forms
# from django_recaptcha.fields import ReCaptchaField

from .validators import validate_password, validate_email, validate_phone


class LoginForm(forms.Form):
    email = forms.CharField(
        widget=forms.EmailInput(attrs={'id': 'email_login_field', 'placeholder': 'Введите Вашу почту'}),
        label='', validators=[validate_email])

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'id': 'password_login_field', 'placeholder': 'Введите пароль'}), label='')


# error_messages={'required': 'Не указано контактное лицо'},
# error_messages={'required': 'Не указан email'},
# error_messages={'required': 'Введите пароль'},
# error_messages={'required': 'Не указан телефон'},
class RegisterForm(forms.Form):
    name = forms.CharField(
        max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Контактное лицо'}), label='')
    phone = forms.CharField(
                            widget=forms.TextInput(attrs={'placeholder': 'Контактное лицо'}),
                            validators=[validate_phone], label='')
    email = forms.CharField(
                            widget=forms.EmailInput(
                                attrs={'id': 'email_register_field', 'placeholder': 'Введите Вашу почту'}),
                            validators=[validate_email], label='')
    password = forms.CharField(
                               widget=forms.PasswordInput(
                                   attrs={'id': 'password_register_field', 'placeholder': 'Введите пароль'}),
                               validators=[validate_password], label='')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Повторите пароль'}), label='')

    # captcha = ReCaptchaField(label='')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        if password and password2 and password != password2:
            self.add_error('password2', 'Пароли не совпадают')


class EmailResetForm(forms.Form):
    email = forms.CharField(
        label='', widget=forms.EmailInput(attrs={'id': 'email_reset_field', 'placeholder': 'Введите Вашу почту'}))
    # captcha = CaptchaField(
    #     label='',
    #     widget=CaptchaTextInput(attrs={'id': 'captcha_reset_field', 'placeholder': 'Введите текст с картинки'}))
