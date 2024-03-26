from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404

from advertisement.models import Advertisement, Region, Category, Store
from advertisement.utils import get_region_variables, sorted_by, sorted_by_number, get_view_type, \
    sorted_by_date_or_price, variables_for_paginator, get_view_type_for_store


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


def get_stores_page(request):
    region_filter, region_param, region_bread_crumbs = get_region_variables(request.GET.get('region'))
    category_list = Category.objects.filter(level__lte=1)
    store_queryset = Store.objects.filter(is_active=True, **region_filter).select_related('category', 'region')
    category_queryset = Category.objects.add_related_count(Category.objects.root_nodes(),
                                                           Store,
                                                           'category',
                                                           'store_counts',
                                                           cumulative=True,
                                                           extra_filters={"region__in": region_filter['region__in'],})
    paginator = Paginator(store_queryset, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "stores_found": store_queryset.count(),
        "category": category_queryset,
        "region_bread_crumbs": region_bread_crumbs,
        "region_param": region_param,
        "category_list": category_list,
        "page_obj": page_obj
    }
    return render(request, 'stores.html', context)


def get_stores_by_category(request, category_slug):
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
    category_queryset = category_queryset_an.filter(parent_id=category.id)
    print(category_queryset)
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

    return response


def get_help_page(request):
    category_list = Category.objects.filter(level__lte=1)
    context = {
        "category_list": category_list
    }
    return render(request, 'help.html', context)
