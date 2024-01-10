from django.shortcuts import render

# Create your views here.


def get_main_page(request):
    return render(request, 'main.html')

def get_help_page(request):
    return render(request, 'help.html')