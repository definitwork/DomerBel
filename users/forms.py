from django.forms import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from .models import User


class UserRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['first_name', 'phone_number', 'email', 'password1', 'password2']
