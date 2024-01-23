from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordResetView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers import AuthSerializer


def logout_view(request):
    logout(request)
    return redirect('home')


class LoginAjaxView(APIView):
    def post(self, request):
        if request.method == 'POST':
            return
