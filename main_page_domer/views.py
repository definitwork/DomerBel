from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.shortcuts import render

from users.forms import EditProfileForm
from advertisement.models import Advertisement, Region, Category


def get_main_page(request):
    advertisement_queryset = Advertisement.objects.filter(
        is_active=True, moderated=True).select_related(
        'category', 'region').order_by("-date_of_create")[:10]
    regions_queryset = Region.objects.filter(level=0)
    category_list = Category.objects.filter(level__lte=1)
    context = {
        "adver": advertisement_queryset,
        "category_list": category_list,
        "regions": regions_queryset,
    }
    return render(request, 'main.html', context)


def get_help_page(request):
    return render(request, 'help.html')


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
                messages.success(request, 'Данные успешно изменены!1')
                messages.success(request, 'Пароль успешно изменен')
            if check_password(password, user.password):
                messages.error(request, 'Ошибка пароля')
            else:
                form.save()
                messages.success(request, 'Данные успешно изменены!')
        else:
            messages.success(request, 'Ошибка смены пароля')
    else:
        form = EditProfileForm(instance=user)

    return render(request, 'personal_account/user_data.html', {'form': form})
