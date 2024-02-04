
from django.shortcuts import render, redirect
from advertisement.forms import StoreForm
from advertisement.models import Advertisement, Region, Category
from users.forms import RegisterForm, LoginForm


# Использую на главной вьюшке 2 формы связанные с юзером
# для того что бы при вызове главной страницы они отрендерелись в pop-up окнах

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect
from advertisement.models import Advertisement, Region
from users.forms import EditProfileForm


# Create your views here.


def get_main_page(request):
    advertisement_queryset = Advertisement.objects.filter(
        is_active=True, moderated=True).select_related(
        'category', 'region').order_by("-date_of_create")[:7]
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

    return render(request, 'user_data.html', {'form': form})


def get_incoming_page(request):
    return render(request, 'incoming_messages.html')


def get_outgoing_page(request):
    return render(request, 'outgoing_messages.html')


def get_sent_page(request):
    return render(request, 'sent_messages.html')


def get_admin_message_page(request):
    return render(request, 'admin_message.html')

# Сохранение экземпляра нового магазина через форму
def add_store(request):
    if request.method == 'POST':
        new_store = StoreForm(request.POST, request.FILES)
        if new_store.is_valid():
            store = new_store.save(commit=False)
            store.user = request.user
            store.save()
            return redirect('personal_account')
        else:
            print(new_store.errors)
    oblast = Region.objects.filter(type='Область')
    store_form = StoreForm(initial={'contact_name': request.user.first_name, 'email': request.user.email,
                                    'phone_num': request.user.phone_number})
    context = {"oblast": oblast,
               "store_form": store_form}
    return render(request, 'add_store.html', context)


def get_my_store(request):
    return render(request, 'my_store.html')