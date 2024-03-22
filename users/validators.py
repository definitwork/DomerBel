from curses.ascii import islower
import re

from django.forms import forms

from users.models import User


def validate_phone(phone_number):
    # Валидация белорусского номера телефона
    if not re.match(r'^(\+375|80)(29|25|44|33)(\d{3})(\d{2})(\d{2})$', phone_number):
        raise forms.ValidationError('Некорректный ввод номера телефона')


def validate_password(password_string):
    if not re.match(r'^(?=.*[A-Z])(?=.*[0-9]).{8,}$', password_string):
        raise forms.ValidationError(
            'Пароль должен быть не меньше 8 симвалов \n В пароле дожны быть маленькие и большие символы \n Пароль не может сотоять только из цифр ')

def validate_email(email):
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        raise forms.ValidationError('Некорректный адрес электронной почты')
    check_email = User.objects.filter(email=email)
    if check_email.exists():
         raise forms.ValidationError('Пользователь с таким email уже зарегистрирован. Войдите в личный кабинет')


     
