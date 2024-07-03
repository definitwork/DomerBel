import codecs
import json
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from .models import Advertisement, Category, Region, Spisok, Element, ElementTwo, Field
from .utils import sorted_by_number, variables_for_paginator, sorted_by_date_or_price, sorted_by, get_view_type, \
    get_region_variables
from .forms import UploadFileForm
from .models import UploadFile
import openpyxl
from zipfile import ZipFile
from advertisement.functions_for_bulk_import import save_many_ads_from_excel, save_many_ads_from_zip
from django.http import FileResponse

def get_advertisement_page(request):
    order_by = sorted_by(request.COOKIES.get('sorted_by'))
    sort_for_paginator = sorted_by_number(request.COOKIES.get('sort'))
    state_sort_by_date = request.COOKIES.get('date', 0)
    view_type, html = get_view_type(request.COOKIES)
    region_filter, region_param, region_bread_crumbs = get_region_variables(request.GET.get('region'))

    if request.GET.get('date') or request.GET.get('price'):
        state_sort_by_date, order_by = sorted_by_date_or_price(request.GET)
    if request.GET.get('sort'):
        sort_for_paginator = sorted_by_number(request.GET.get('sort'))
    if request.GET.get('view_type'):
        view_type, html = get_view_type(request.GET)

    category_list = Category.objects.filter(level__lte=1)
    advertisement_queryset = Advertisement.objects.filter(is_active=True,
                                                          moderated=True, **region_filter).select_related(
        'category',
        'region').order_by(order_by)
    category_queryset = Category.objects.add_related_count(Category.objects.root_nodes(),
                                                           Advertisement,
                                                           'category',
                                                           'advertisement_counts',
                                                           cumulative=True,
                                                           extra_filters={"region__in": region_filter['region__in']})

    page_obj = variables_for_paginator(advertisement_queryset,
                                       request.GET.get('page'),
                                       sort_for_paginator)

    context = {
        "ads_found": advertisement_queryset.count(),
        "category": category_queryset,
        "category_list": category_list,
        "region_bread_crumbs": region_bread_crumbs,
        "region_param": region_param,
        "page_obj": page_obj,
        'date': state_sort_by_date,
        'view_type': view_type,
        'adaptive_navigation': "Доска объявлений. Беларусь",
    }

    response = render(request, html, context)
    response.set_cookie('sort', sort_for_paginator)
    response.set_cookie('date', state_sort_by_date)
    response.set_cookie('sorted_by', order_by)
    response.set_cookie('view_type', view_type)
    response.set_cookie('user_auth', request.user.id)

    return response


def get_advertisement_by_category(request, category_slug):
    order_by = sorted_by(request.COOKIES.get('sorted_by'))
    sort_for_paginator = sorted_by_number(request.COOKIES.get('sort'))
    state_sort_by_date = request.COOKIES.get('date', 0)
    view_type, html = get_view_type(request.COOKIES)
    region_filter, region_param, region_bread_crumbs = get_region_variables(request.GET.get('region'))

    if request.GET.get('date') or request.GET.get('price'):
        state_sort_by_date, order_by = sorted_by_date_or_price(request.GET)
    if request.GET.get('sort'):
        sort_for_paginator = sorted_by_number(request.GET.get('sort'))
    if request.GET.get('view_type'):
        view_type, html = get_view_type(request.GET)

    category_queryset_all = Category.objects.all()
    category_list = category_queryset_all.filter(level__lte=1)
    category = get_object_or_404(category_queryset_all, slug=category_slug)
    category_bread_crumbs = category.get_ancestors(ascending=False, include_self=True)
    category_queryset_an = Category.objects.add_related_count(category.get_descendants(),
                                                              Advertisement,
                                                              'category',
                                                              'advertisement_counts',
                                                              cumulative=True,
                                                              extra_filters={"region__in": region_filter['region__in']})
    category_queryset = category_queryset_an.filter(parent_id=category.id)
    advertisement_queryset = Advertisement.objects.filter(Q(category__in=category_queryset_an) |
                                                          Q(category__slug=category.slug),
                                                          **region_filter,
                                                          is_active=True,
                                                          moderated=True).select_related(
        'category',
        'region').order_by(order_by)
    page_obj = variables_for_paginator(advertisement_queryset,
                                       request.GET.get('page'),
                                       sort_for_paginator)
    context = {
        "ads_found": advertisement_queryset.count(),
        "category": category_queryset,
        "region_param": region_param,
        "category_bread_crumbs": category_bread_crumbs,
        "region_bread_crumbs": region_bread_crumbs,
        "category_list": category_list,
        "page_obj": page_obj,
        'date': state_sort_by_date,
        'view_type': view_type,
        'adaptive_navigation': f"{category.main_title if category.main_title else category.title}. Беларусь",
    }

    response = render(request, html, context)
    response.set_cookie('sort', sort_for_paginator)
    response.set_cookie('date', state_sort_by_date)
    response.set_cookie('sorted_by', order_by)
    response.set_cookie('view_type', view_type)

    return response


def get_page_place_an_ad(request):
    category_list = Category.objects.filter(level__lte=1)

    context = {
        "category_list": category_list,
        'adaptive_navigation': "Добавление объявления",
    }
    
    return render(request, 'place_an_ad.html', context)


def get_page_place_an_favorites(request):
    context = {}
    category_list = Category.objects.filter(level__lte=1)
    context["category_list"] = category_list
    json_data = request.GET.get('list')
    data = json.loads(json_data)
    

    if len(data):
        objects = Advertisement.objects.filter(pk__in=data)
        context['objects'] = objects
        context['cards_num'] = len(objects)

    return render(request, 'place_an_favorites.html', context)


def get_bulk_import_of_ads(request):
    """Страница массового импорта объявлений"""
    context = {
        'form': UploadFileForm(),
    }
    '''Проверь физ лицо или юр лицо!!!!!!'''
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            if form.cleaned_data.get("file").name.endswith('xlsx'):
                '''Работа с электронной таблицей'''
                try:
                    uploud_file = form.cleaned_data.get("file")
                    book = openpyxl.open(uploud_file,read_only=True)
                    save_file = UploadFile(file=uploud_file, user=request.user)
                    save_file.save()
                    ads = save_many_ads_from_excel(f'./media/{save_file.file.name}',request.user)
                    save_file.delete()
                    if ads != True:
                        file_error = ads.get('file')
                        '''ТУТ надо отдать файл  ошибками пользователю'''
                        return FileResponse(open(file_error, "rb"))
                    else:
                        context['answer'] = 'Объявления успешно сохранены'
                except:
                    context['answer'] = 'Невозможно прочитать файл.'
            elif form.cleaned_data.get("file").name.endswith('zip'):
                '''Работа с электронным архивом'''
                try:
                    uploud_zip = form.cleaned_data.get("file")
                    with ZipFile(uploud_zip,'r') as zip:
                        files_from_zip = zip.namelist()
                    save_zip = UploadFile(file=uploud_zip, user=request.user)
                    save_zip.save()
                    ads = save_many_ads_from_zip(f'./media/{save_zip.file.name}', request.user)
                    save_zip.delete()
                    if ads != True:
                        file_error = ads.get('file')
                        context['answer'] = 'Несколько объявлений не были сохранены. Чтобы посмотреть объявления с ошибками скачайте файл.'
                        context['file'] = 1
                    else:
                        context['answer'] = 'Объявления успешно сохранены'

                except:
                    print('не прошла проверка')
                    context['answer'] = 'Невозможно прочитать файл'
        else:
            context['error'] = 'Ошибка при загрузке файла. Убедитесь, что загружаемый файл необходимого расширения'
    else:
        form = UploadFileForm()
    return render(request=request,
                  template_name='bulk_import_ads.html',
                  context = context)

# def download_file_with_error_ads(request):
#     '''Отдает файл с объявлениями, где найдены были ошибки, при массовом импорте объявлений'''
#     if request.method == 'GET':
#         email = request.user.email
#         path = f'./media/files_for_bulk_import_of_ads/{email}/error_{email}.xlsx'
#         return FileResponse(open(path, "rb"))




def get_advertisement_details_page(request, id):
    '''Отдаем страничку с детальным описанием объявления'''
    advertisement = Advertisement.objects.get(id=id)
    category_queryset_all = Category.objects.all()
    category_list = category_queryset_all.filter(level__lte=1)
    context = {
        "category_list": category_list,
        'advertisement': advertisement,
    }
    return render(request=request,
                  template_name='advertisement_details.html',
                  context=context)



def get_instructions_for_bulk_import_of_ads(request):
    regions = Region.objects.all()
    categories = Category.objects.prefetch_related('field_set').all()
    fields = categories.fielf_set.all()

    context = {}
    return render(request=request,
                  template_name='instructions_for_bulk_import_of_ads.html',
                  context=context)