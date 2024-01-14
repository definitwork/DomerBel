from django.shortcuts import render

# Create your views here.


def get_main_page(request):
    return render(request, 'main.html')

def get_help_page(request):
    return render(request, 'help.html')

def get_personal_account_page(request):
    return render(request, 'personal_account.html')

def get_user_data_page(request):
    return  render(request, 'user_data.html')