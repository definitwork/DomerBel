from django.core.paginator import Paginator


def sorted_by_number(number):
    if (number == '30'
            or number == '60'
            or number == '90'):
        sort_for_paginator = int(number)
        return sort_for_paginator
    else:
        return 3


def variables_for_paginator(queryset, page=1, elments=30):
    paginator = Paginator(queryset, elments)
    page_number = page
    page_obj = paginator.get_page(page_number)
    return page_obj


def sorted_by_date_or_price(sort):
    if sort.get('date'):
        if sort['date'] == '0':
            return (1, 'date_of_create')
        else:
            return (0, '-date_of_create')
    elif sort.get('price'):
        if sort['price'] == '0':
            return (1, 'price')
        else:
            return (0, '-price')


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
                return (1, 'advertisement_page_type_2.html')
            else:
                return (0, 'advertisement_page_type_1.html')
        elif view_type.get('view_type'):
            if view_type.get('view_type') == '0':
                return (1, 'advertisement_page_type_2.html')
            else:
                return (0, 'advertisement_page_type_1.html')
        else:
            return (0, 'advertisement_page_type_1.html')
    else:
        return (0, 'advertisement_page_type_1.html')
