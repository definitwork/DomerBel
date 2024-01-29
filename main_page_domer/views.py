from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect
from advertisement.models import Advertisement, Region
from users.forms import EditProfileForm
from users.validators import validate_password


# Create your views here.

def get_main_page(request):
    advertisement_queryset = Advertisement.objects.filter(
        is_active=True, moderated=True).select_related(
        'category', 'region', 'images').order_by("-date_of_create")[:7]
    regions_queryset = Region.objects.all()
    context = {"adver": advertisement_queryset, }
    return render(request, 'main.html', context)


def get_help_page(request):
    return render(request, 'help.html')


def get_personal_account_page(request):
    return render(request, 'personal_account.html')


@login_required
def get_user_data_page(request):
    user = request.user
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=user)
        if form.is_valid():
            password = form.cleaned_data.get('password')
            new_password = form.cleaned_data.get('new_password')
            repeat_password = form.cleaned_data.get('repeat_password')
            if check_password(password, user.password) and new_password != '' and repeat_password != '':
                user.set_password(new_password)
                user.save()
                form.save()
                messages.success(request, 'Данные успешно изменены!')
                messages.success(request, 'Пароль успешно изменен')
            else:
                if not check_password(password, user.password):
                    messages.error(request, 'Ошибка пароля')
                else:
                    form.save()
                    messages.success(request, 'Данные успешно изменены!')
                return redirect('ud')
    else:
        form = EditProfileForm(instance=user)

    return render(request, 'user_data.html', {'form': form})


def get_incoming_page(request):
    return render(request, 'incoming_messages.html')


def get_outgiong_page(request):
    return render(request, 'outgiong_messages.html')


def get_sent_page(request):
    return render(request, 'sent_messages.html')


def get_admin_message_page(request):
    return render(request, 'admin_message.html')
