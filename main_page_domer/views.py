from django.shortcuts import render

from advertisement.models import Advertisement, Region


# Create your views here.


def get_main_page(request):
    advertisement_queryset = Advertisement.objects.filter(is_active=True, moderated=True).select_related('category', 'region', 'images').order_by("-date_of_create")[:7]
    regions_queryset = Region.objects.all()
    context = {
        "adver": advertisement_queryset,
        "regions": regions_queryset,

    }
    return render(request, 'main.html', context)

def get_help_page(request):
    return render(request, 'help.html')

def get_personal_account_page(request):
    return render(request, 'personal_account.html')

def get_user_data_page(request):
    return render(request, 'user_data.html')

def get_incoming_page(request):
    return render(request, 'incoming_messages.html')

def get_outgiong_page(request):
    return render(request, 'outgiong_messages.html')

def get_sent_page(request):
    return render(request, 'sent_messages.html')

def get_admin_message_page(request):
    return render(request, 'admin_message.html')