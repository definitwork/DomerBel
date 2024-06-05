import re

from rest_framework import serializers


def validate_password(password_string):
    if not re.match(r'^(?=.*[A-Z])(?=.*[0-9]).{8,}$', password_string):
        if len(password_string) < 8:
            raise serializers.ValidationError('Пароль слишком короткий')
        if str(password_string).isdigit():
            raise serializers.ValidationError('Пароль не может состоять только из цифр')
        if str(password_string).isalpha():
            raise serializers.ValidationError('В пароле должна быть хотя бы одна цифра')
        if str(password_string).isupper():
            raise serializers.ValidationError('В пароле должен быть хотя бы один символ нижнего регистра')
        if str(password_string).islower():
            raise serializers.ValidationError('В пароле должен быть хотя бы один символ верхнего регистра')