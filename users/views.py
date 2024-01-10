from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm


def register(request):
    if request.method == "POST":
        print(request.POST)
    #     form = UserRegisterForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return redirect("login")
    # else:
    #     form = UserRegisterForm()
        return render(request, 'users/profile.html')


@login_required
def profile(request):
    return render(request, template_name='users/profile.html')
