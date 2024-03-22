import codecs
import json

from django.db.models import Q
from django.shortcuts import render, get_object_or_404

from .models import Advertisement, Category, Region, Spisok, Element, ElementTwo, Field

from .utils import sorted_by_number, variables_for_paginator, sorted_by_date_or_price, sorted_by, get_view_type, \
    get_region_variables


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
    }

    response = render(request, html, context)
    response.set_cookie('sort', sort_for_paginator)
    response.set_cookie('date', state_sort_by_date)
    response.set_cookie('sorted_by', order_by)
    response.set_cookie('view_type', view_type)

    return response


def get_page_place_an_ad(request):
    oblast = Region.objects.filter(type='Область')
    spisok = Spisok.objects.all()
    category = Category.objects.all()



    context = {
        'spisok': spisok,
        'oblast': oblast,
        'category': category,
    }
    return render(request, 'place_an_ad.html', context)
