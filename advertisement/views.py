import json

from django.db.models import Q
from django.shortcuts import render, get_object_or_404

from .models import Advertisement, Category, Region

from .utils import sorted_by_number, variables_for_paginator, sorted_by_date_or_price, sorted_by, get_view_type


def load_new_region_to_model(request):
    with open('./region_refactor_id.json') as json_file:
        ishod_dump = json.loads(json_file.read())
        for i in ishod_dump:
            # id = i['id_region']
            area = i['region']
            type = i['rayon']
            slug = i['url']
            parent_id = i['parent_id']

            region = Region(id=id, area=area, type=type, slug=slug, parent_id=parent_id)
            print(region)
            print(area, type, slug, parent_id)
        return render(request, '1111.html')


# Create your views here.

def get_advertisement_page(request):
    order_by = sorted_by(request.COOKIES.get('sorted_by'))
    sort_for_paginator = sorted_by_number(request.COOKIES.get('sort'))
    state_sort_by_date = request.COOKIES.get('date', 0)
    view_type, html = get_view_type(request.COOKIES)

    if request.GET.get('date') or request.GET.get('price'):
        state_sort_by_date, order_by = sorted_by_date_or_price(request.GET)
    if request.GET.get('sort'):
        sort_for_paginator = sorted_by_number(request.GET.get('sort'))
    if request.GET.get('view_type'):
        view_type, html = get_view_type(request.GET)

    category_list = Category.objects.filter(level__lte=1)
    advertisement_queryset = Advertisement.objects.filter(is_active=True,
                                                          moderated=True).select_related(
        'category',
        'region').order_by(order_by)
    category_queryset = Category.objects.add_related_count(Category.objects.root_nodes(),
                                                           Advertisement,
                                                           'category',
                                                           'advertisement_counts',
                                                           cumulative=True)

    page_obj = variables_for_paginator(advertisement_queryset,
                                       request.GET.get('page'),
                                       sort_for_paginator)
    context = {
        "category": category_queryset,
        "category_list": category_list,
        "page_obj": page_obj,
        'date': state_sort_by_date,
        'view_type': view_type,
    }

    response = render(request, html, context)
    response.set_cookie('sort', sort_for_paginator)
    response.set_cookie('date', state_sort_by_date)
    response.set_cookie('sorted_by', order_by)
    response.set_cookie('view_type', view_type)

    return response


def get_advertisement_by_category(request, category_slug):
    order_by = sorted_by(request.COOKIES.get('sorted_by'))
    sort_for_paginator = sorted_by_number(request.COOKIES.get('sort'))
    state_sort_by_date = request.COOKIES.get('date', 0)
    view_type, html = get_view_type(request.COOKIES)

    if request.GET.get('date') or request.GET.get('price'):
        state_sort_by_date, order_by = sorted_by_date_or_price(request.GET)
    if request.GET.get('sort'):
        sort_for_paginator = sorted_by_number(request.GET.get('sort'))
    if request.GET.get('view_type'):
        view_type, html = get_view_type(request.GET)

    category_queryset_all = Category.objects.all()
    category_list = category_queryset_all.filter(level__lte=1)
    category = get_object_or_404(category_queryset_all, slug=category_slug)
    category_queryset_an = Category.objects.add_related_count(category.get_descendants(),
                                                              Advertisement,
                                                              'category',
                                                              'advertisement_counts',
                                                              cumulative=True)
    category_queryset = category_queryset_an.filter(parent_id=category.id)
    advertisement_queryset = Advertisement.objects.filter(Q(category__in=category_queryset_an) |
                                                          Q(category__slug=category.slug),
                                                          is_active=True,
                                                          moderated=True).select_related(
        'category',
        'region').order_by(order_by)
    page_obj = variables_for_paginator(advertisement_queryset,
                                       request.GET.get('page'),
                                       sort_for_paginator)
    context = {
        "category": category_queryset,
        "category_list": category_list,
        "page_obj": page_obj,
        'date': state_sort_by_date,
        'view_type': view_type,
    }

    response = render(request, html, context)
    response.set_cookie('sort', sort_for_paginator)
    response.set_cookie('date', state_sort_by_date)
    response.set_cookie('sorted_by', order_by)
    response.set_cookie('view_type', view_type)

    return response
# Create your views here.
