import re

from django.forms import forms


def validate_phone(phone_number):
    # Валидация белорусского номера телефона
    if not re.match(r'^(\+375|80)(29|25|44|33)(\d{3})(\d{2})(\d{2})$', phone_number):
        raise forms.ValidationError('Некорректный ввод номера')


def validate_password(password_string):
    if not re.match(r'^(?=.*[A-Z])(?=.*[0-9]).{8,}$', password_string):
        raise forms.ValidationError('Некорректный ввод пароля')


def validate_email(email):
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        raise forms.ValidationError('Некорректный адрес электронной почты')
