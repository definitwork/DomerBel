from django.shortcuts import render, redirect
from advertisement.forms import StoreForm
from advertisement.models import Advertisement, Region, Category
from users.forms import UserRegisterForm, CustomAuthenticationForm, SendEmailForm


# Использую на главной вьюшке 2 формы связанные с юзером
# для того что бы при вызове главной страницы они отрендерелись в pop-up окнах
def get_main_page(request):
    advertisement_queryset = Advertisement.objects.filter(
        is_active=True, moderated=True).select_related(
        'category', 'region', 'images').order_by("-date_of_create")[:7]

    regions_queryset = Region.objects.filter(type='Область')
    reg_form = UserRegisterForm()
    login_form = CustomAuthenticationForm()
    email_form = SendEmailForm()
    context = {
        "adver": advertisement_queryset,
        "regions": regions_queryset,
        "reg_form": reg_form,
        "login_form": login_form,
        'email_form': SendEmailForm
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