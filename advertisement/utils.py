from django.core.paginator import Paginator

from advertisement.models import Region


def sorted_by_number(number):
    if (number == '3'
            or number == '6'
            or number == '9'):
        sort_for_paginator = int(number)
        return sort_for_paginator
    else:
        return 3


def variables_for_paginator(queryset, page=1, elements=30):
    paginator = Paginator(queryset, elements)
    page_number = page
    page_obj = paginator.get_page(page_number)
    return page_obj


def sorted_by_date_or_price(sort):
    if sort.get('date'):
        if sort['date'] == '0':
            return 1, 'date_of_create'
        else:
            return 0, '-date_of_create'
    elif sort.get('price'):
        if sort['price'] == '0':
            return 1, 'price'
        else:
            return 0, '-price'


def sorted_by(key):
    if key == '-date_of_create' or key == 'date_of_create' or key == 'price' or key == '-price':
        return key
    else:
        return '-date_of_create'


def get_view_type(view_type):
    if view_type.get('view_type'):
        view_type = view_type.get('view_type')
        if type(view_type) == str:
            if view_type == '1':
                return 1, 'advertisement_page_type_2.html'
            else:
                return 0, 'advertisement_page_type_1.html'
        elif view_type.get('view_type'):
            if view_type.get('view_type') == '0':
                return 1, 'advertisement_page_type_2.html'
            else:
                return 0, 'advertisement_page_type_1.html'
        else:
            return 0, 'advertisement_page_type_1.html'
    else:
        return 0, 'advertisement_page_type_1.html'


def get_region_variables(region_request):
    if region_request:
        region_filter = dict(
            region__in=Region.objects.filter(id=region_request).get_descendants(include_self=True))
        region_param = region_filter.get("region__in").get(id=region_request)
        region_bread_crumbs = region_param.get_ancestors(ascending=False, include_self=True)
        return region_filter, region_param, region_bread_crumbs
    else:
        region_filter = dict(region__in=Region.objects.all())
        region_bread_crumbs = ''
        region_param = ''
        return region_filter, region_param, region_bread_crumbs


def get_view_type_for_store(view_type):
    if view_type.get('view_type'):
        view_type = view_type.get('view_type')
        if type(view_type) == str:
            if view_type == '1':
                return 1, 'store_detail_page_type_2.html'
            else:
                return 0, 'store_detail_page_type_1.html'
        elif view_type.get('view_type'):
            if view_type.get('view_type') == '0':
                return 1, 'store_detail_page_type_2.html'
            else:
                return 0, 'store_detail_page_type_1.html'
        else:
            return 0, 'store_detail_page_type_1.html'
    else:
        return 0, 'store_detail_page_type_1.html'