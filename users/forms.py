from django import forms


class LoginAjaxForm(forms.Form):
    email = forms.CharField(label='Электронная почта',
                            widget=forms.EmailInput(attrs={'placeholder': 'Введите Вашу почту'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль'}), label='Пароль')
