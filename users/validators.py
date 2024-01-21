import re

from django.forms import forms


def validate_phone(phone_number):
    # Валидация белорусского номера телефона
    if not re.match(r'^(\+375|80)(29|25|44|33)(\d{3})(\d{2})(\d{2})$', phone_number):
        raise forms.ValidationError('наконец то!!!')

# def validate_not_empty(value):
#     # Проверка "а заполнено ли поле?"
#     if value == '':
#         raise forms.ValidationError(
#             'А кто поле будет заполнять, Пушкин?',
#             params={'value': value},
