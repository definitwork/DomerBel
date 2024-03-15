from django.contrib.auth import logout, authenticate, login, get_user_model
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, render


from main_page_domer.forms import StoreForm
from main_page_domer.models import Store
from advertisement.models import Region, Category
from .forms import LoginForm, RegisterForm
from .models import User


def get_personal_account_page(request):
    category_list = Category.objects.filter(level__lte=1)
    context = {
        "category_list": category_list,
    }
    return render(request, 'personal_account/personal_account.html', context)


def get_incoming_page(request):
    category_list = Category.objects.filter(level__lte=1)
    context = {
        "category_list": category_list,
    }
    return render(request, 'personal_account/incoming_messages.html', context)


def get_outgoing_page(request):
    category_list = Category.objects.filter(level__lte=1)
    context = {
        "category_list": category_list,
    }
    return render(request, 'personal_account/outgoing_messages.html', context)


def get_sent_page(request):
    category_list = Category.objects.filter(level__lte=1)
    context = {
        "category_list": category_list,
    }
    return render(request, 'personal_account/sent_messages.html', context)


def get_admin_message_page(request):
    category_list = Category.objects.filter(level__lte=1)
    context = {
        "category_list": category_list,
    }
    return render(request, 'personal_account/admin_message.html', context)


# Сохранение экземпляра нового магазина через форму
def add_store(request):
    if request.method == 'POST':
        new_store = StoreForm(request.POST, request.FILES)
        if new_store.is_valid():
            store = new_store.save(commit=False)
            store.user = request.user
            store.save()
            messages.success(request, f"Новый магазин {store} успешно создан!")
            return redirect('users:my_store')

        oblast = Region.objects.filter(type='Область')
        store_form = StoreForm(request.POST, request.FILES)
        store_form.errors.update(new_store.errors)
        category_list = Category.objects.filter(level__lte=1)
        context = {"oblast": oblast,
                   "store_form": store_form,
                   "category_list": category_list}
        return render(request, 'personal_account/add_store.html', context)


    oblast = Region.objects.filter(type='Область')
    store_form = StoreForm(initial={'contact_name': request.user.first_name, 'email': request.user.email,
                                    'phone_num': request.user.phone_number})
    category_list = Category.objects.filter(level__lte=1)

    context = {"oblast": oblast,
               "store_form": store_form,
               "category_list": category_list}
    return render(request, 'personal_account/add_store.html', context)


# Показывает в личном кабинете все магазины, которые создал пользователь
def get_my_store(request):
    stores = Store.objects.filter(user=request.user).order_by('id')
    category_list = Category.objects.filter(level__lte=1)
    oblast_list = []
    if stores.exists():
        context = {
            'stores': stores,
            'oblast_list': oblast_list,
            'category_list': category_list,
        }
    else:
        context = {}
    return render(request, 'personal_account/my_store.html', context)


def get_store_page(request, slug):
    store_page = Store.objects.get(user=request.user, slug=slug)
    oblast = Region.objects.get(id=store_page.region.parent_id)
    category_list = Category.objects.filter(level__lte=1)
    context = {
        'store_page': store_page,
        'oblast': oblast,
        'category_list': category_list
    }
    return render(request, 'personal_account/store_page.html', context)


# Редактирование экземпляра магазина через форму
def edit_store(request, store_id):
    store = Store.objects.get(user=request.user, id=store_id)
    if request.method == 'POST':
        edit_store = StoreForm(request.POST, request.FILES, instance=store)
        if edit_store.is_valid():
            updated_store = edit_store.save(commit=False)
            updated_store.user = request.user
            updated_store.save()
            messages.success(request, f"Магазин {store} успешно изменён!")
            return redirect('users:my_store')

    else:
        edit_store = StoreForm(instance=store)

    oblast = Region.objects.filter(type='Область')
    selected_oblast = Region.objects.get(id=store.region.parent_id)
    categories = Category.objects.all()
    category_list = Category.objects.filter(level__lte=1)
    context = {
        'edit_store': edit_store,
        'oblast': oblast,
        'selected_oblast': selected_oblast,
        'categories': categories,
        'selected_category': store.category.id if store.category else None,
        'store': store,
        'category_list': category_list
    }
    return render(request, 'personal_account/edit_store.html', context)


# Удаление экземпляра магазина
def delete_store(request, store_id):
    store = Store.objects.get(user=request.user, id=store_id)
    if request.method == "POST":
        store.delete()
        messages.success(request, f"Магазин {store} успешно удален!")
        return redirect('users:my_store')
    context = {'store': store}
    return render(request, 'personal_account/delete_store.html', context)


def logout_view(request):
    logout(request)
    return redirect('home')


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'errors': 1})
        else:
            return JsonResponse({'errors': 1})


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User()
            user.first_name = form.cleaned_data.get('name')
            user.phone_number = form.cleaned_data.get('phone')
            user.email = form.cleaned_data.get('email')
            user.set_password(form.cleaned_data.get('password'))
            user.set_password(form.cleaned_data.get('password2'))
            user.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'errors': form.errors})