from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect

from users.forms import EditProfileForm
from advertisement.forms import StoreForm
from advertisement.models import Advertisement, Region, Store, Category


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
    store = Store.objects.get(user=request.user)
    oblast = Region.objects.get(id=store.region.parent_id)
    start_date = store.date_of_create
    end_date = store.date_of_deactivate
    days_till_expiration = end_date - start_date
    context = {
        'store': store,
        'oblast': oblast,
        'days_till_expiration': days_till_expiration.days
    }
    return render(request, 'my_store.html', context)

def get_store_page(request, slug):
    store_page = Store.objects.get(user=request.user, slug=slug)
    oblast = Region.objects.get(id=store_page.region.parent_id)
    context = {
        'store_page': store_page,
        'oblast': oblast
    }
    return render(request, 'store_page.html', context)

def edit_store(request):
    store = Store.objects.get(user=request.user)
    if request.method == 'POST':
        edit_store = StoreForm(request.POST, request.FILES, instance=store)
        if edit_store.is_valid():
            updated_store = edit_store.save(commit=False)
            updated_store.user = request.user
            updated_store.save()
    else:
        edit_store = StoreForm(instance=store)
    oblast = Region.objects.filter(type='Область')
    selected_oblast = Region.objects.get(id=store.region.parent_id)
    categories = Category.objects.all()
    context = {
        'edit_store': edit_store,
        'oblast': oblast,
        'selected_oblast': selected_oblast,
        'categories': categories,
        'selected_category': store.category.id if store.category else None,
        'store':store,
    }
    return render(request, 'edit_store.html', context)