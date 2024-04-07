from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect

from advertisement.models import Advertisement, Region, Category, Store
from advertisement.utils import get_region_variables, sorted_by, sorted_by_number, get_view_type, \
    sorted_by_date_or_price, variables_for_paginator, get_view_type_for_store


def get_main_page(request):
    """ Отдаём главную страницу """
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


def get_stores_page(request):
    """ Страница со всеми магазинами сайта """
    locations = Region.objects.filter(type='Область')
    category_list = Category.objects.filter(level__lte=1)
    store_queryset = Store.objects.filter(is_active=True).select_related('category', 'region')
    category_queryset = Category.objects.add_related_count(Category.objects.root_nodes(),
                                                           Store,
                                                           'category',
                                                           'store_counts',
                                                           cumulative=True)
    paginator = Paginator(store_queryset, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "stores_found": store_queryset.count(),
        "category": category_queryset,
        "category_list": category_list,
        "locations": locations,
        "page_obj": page_obj
    }

    return render(request, 'stores.html', context)


def get_store_search(request):
    """ Отдаем страницу с результатами поиска по магазинам"""
    category_1 = request.GET.get("category_1")
    category_2 = request.GET.get("category_2")
    search_text = request.GET.get("search_text")
    region_1 = request.GET.get("region_1")
    region_2 = request.GET.get("region_2")
    dict_for_filter = {}
    if category_1 != "0":
        dict_for_filter.update({"category__parent__id": category_1})
    if category_2 != "0":
        dict_for_filter.update({"category__id": category_2})
    if len(search_text) >= 3:
        dict_for_filter.update({"description__icontains": search_text})
    if region_1 != "0":
        dict_for_filter.update({"region__parent__id": region_1})
    if region_2 != "0":
        dict_for_filter.update({"region__id": region_2})

    store_queryset = Store.objects.filter(is_active=True, **dict_for_filter).select_related('category', 'region')
    category_queryset = Category.objects.add_related_count(Category.objects.root_nodes(),
                                                           Store,
                                                           'category',
                                                           'store_counts',
                                                           cumulative=True)
    locations = Region.objects.filter(type='Область')
    category_list = Category.objects.filter(level__lte=1)

    paginator = Paginator(store_queryset, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "stores_found": store_queryset.count(),
        "category": category_queryset,
        "locations": locations,
        "category_list": category_list,
        "page_obj": page_obj
    }

    return render(request, 'stores_search_results.html', context)


def get_stores_by_category(request, category_slug):
    """Переходы по дочерним категориям магазинов """
    region_filter, region_param, region_bread_crumbs = get_region_variables(request.GET.get('region'))
    category_queryset_all = Category.objects.all()
    category_list = Category.objects.filter(level__lte=1)
    category = get_object_or_404(category_queryset_all, slug=category_slug)
    category_queryset_an = Category.objects.add_related_count(category.get_descendants(),
                                                              Store,
                                                              'category',
                                                              'store_counts',
                                                              cumulative=True,
                                                              extra_filters={"region__in": region_filter['region__in']})
    store_queryset = Store.objects.filter(Q(category__in=category_queryset_an) |
                                                          Q(category__slug=category.slug),
                                                          **region_filter,
                                                          is_active=True).select_related(
                                                          'category',
                                                          'region')
    paginator = Paginator(store_queryset, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "stores_found": store_queryset.count(),
        "category": category_queryset_an,
        "region_bread_crumbs": region_bread_crumbs,
        "region_param": region_param,
        "category_list": category_list,
        "page_obj": page_obj
    }
    return render(request, 'stores_by_category.html', context)


def get_store_by_title(request, store_slug):
    """ Переход на страницу выбранного магазина с его объявлениями """
    order_by = sorted_by(request.COOKIES.get('sorted_by'))
    sort_for_paginator = sorted_by_number(request.COOKIES.get('sort'))
    state_sort_by_date = request.COOKIES.get('date', 0)
    view_type, html = get_view_type_for_store(request.COOKIES)
    region_filter, region_param, region_bread_crumbs = get_region_variables(request.GET.get('region'))

    if request.GET.get('date') or request.GET.get('price'):
        state_sort_by_date, order_by = sorted_by_date_or_price(request.GET)
    if request.GET.get('sort'):
        sort_for_paginator = sorted_by_number(request.GET.get('sort'))
    if request.GET.get('view_type'):
        view_type, html = get_view_type_for_store(request.GET)

    store_page = Store.objects.get(slug=store_slug)
    oblast = Region.objects.get(id=store_page.region.parent_id)
    category_list = Category.objects.filter(level__lte=1)
    advertisement_queryset = Advertisement.objects.filter(store=store_page, is_active=True,
                                                          moderated=True, **region_filter).select_related(
                                                          'category',
                                                          'region').order_by(order_by)
    category_queryset = Category.objects.add_related_count(Category.objects.root_nodes(),
                                                           Advertisement,
                                                           'category',
                                                           'advertisement_counts',
                                                           cumulative=True,
                                                           extra_filters={"region__in": region_filter['region__in'],
                                                                          "category__advertisement__in": advertisement_queryset})

    page_obj = variables_for_paginator(advertisement_queryset,
                                       request.GET.get('page'),
                                       sort_for_paginator)

    context = {
        'store_page': store_page,
        'oblast': oblast,
        "category_list": category_list,
        "ads_found": advertisement_queryset.count(),
        "category": category_queryset,
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
    response.set_cookie('user_auth', request.user.id)

    return response


def get_store_by_title_and_category(request, store_slug, category_slug):
    """ Переходы по дочерним категориям объявлений выбранного магазина """
    order_by = sorted_by(request.COOKIES.get('sorted_by'))
    sort_for_paginator = sorted_by_number(request.COOKIES.get('sort'))
    state_sort_by_date = request.COOKIES.get('date', 0)
    view_type, html = get_view_type_for_store(request.COOKIES)
    region_filter, region_param, region_bread_crumbs = get_region_variables(request.GET.get('region'))

    if request.GET.get('date') or request.GET.get('price'):
        state_sort_by_date, order_by = sorted_by_date_or_price(request.GET)
    if request.GET.get('sort'):
        sort_for_paginator = sorted_by_number(request.GET.get('sort'))
    if request.GET.get('view_type'):
        view_type, html = get_view_type_for_store(request.GET)

    store_page = Store.objects.get(slug=store_slug)
    oblast = Region.objects.get(id=store_page.region.parent_id)
    category_queryset_all = Category.objects.all()
    category_list = Category.objects.filter(level__lte=1)
    category = get_object_or_404(category_queryset_all, slug=category_slug)
    category_bread_crumbs = category.get_ancestors(ascending=False, include_self=True)
    category_queryset_an = Category.objects.add_related_count(category.get_descendants(),
                                                              Advertisement,
                                                              'category',
                                                              'advertisement_counts',
                                                              cumulative=True,
                                                              extra_filters={"region__in": region_filter['region__in'],})
    category_queryset = category_queryset_an.filter(parent_id=category.id)
    advertisement_queryset = Advertisement.objects.filter(Q(category__in=category_queryset_an) |
                                                          Q(category__slug=category.slug), store=store_page,
                                                          **region_filter,
                                                          is_active=True).select_related(
                                                          'category',
                                                          'region')

    page_obj = variables_for_paginator(advertisement_queryset,
                                       request.GET.get('page'),
                                       sort_for_paginator)

    context = {
        'store_page': store_page,
        'oblast': oblast,
        "category_list": category_list,
        "ads_found": advertisement_queryset.count(),
        "category": category_queryset,
        "category_bread_crumbs": category_bread_crumbs,
        "region_bread_crumbs": region_bread_crumbs,
        "region_param": region_param,
        'page_obj': page_obj,
        'date': state_sort_by_date,
        'view_type': view_type,
    }
    response = render(request, html, context)
    response.set_cookie('sort', sort_for_paginator)
    response.set_cookie('date', state_sort_by_date)
    response.set_cookie('sorted_by', order_by)
    response.set_cookie('view_type', view_type)
    response.set_cookie('user_auth', request.user.id)

    return response


def get_help_page(request):
    """ Страница Помощь """
    category_list = Category.objects.filter(level__lte=1)
    context = {
        "category_list": category_list
    }
    return render(request, 'help.html', context)
