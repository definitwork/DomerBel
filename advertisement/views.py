import json
import random
from datetime import datetime, timedelta
from pprint import pprint

from django.contrib.postgres.search import SearchVector
from django.db.models import Q, F
from django.db.models.fields.json import KT
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.utils.timezone import get_current_timezone

from .models import Advertisement, Category, Region, Spisok, Element, ElementTwo, Field

from .utils import sorted_by_number, variables_for_paginator, sorted_by_date_or_price, sorted_by, get_view_type, \
    get_region_variables, where_to_look, search_additional_information, annotating_field


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
        'region').order_by("-raise_in_search", order_by)
    vip_advertisement = advertisement_queryset.filter(vip=True)
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
        "vip_advertisement": vip_advertisement,
        'date': state_sort_by_date,
        'view_type': view_type,
        'adaptive_navigation': "Доска объявлений. Беларусь",
    }

    response = render(request, "advertisementAdd.html", context)
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
    vip_advertisement = advertisement_queryset.filter(vip=True)
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
        "vip_advertisement": vip_advertisement,
        'date': state_sort_by_date,
        'view_type': view_type,
        'adaptive_navigation': f"{category.main_title if category.main_title else category.title}. Беларусь",
    }

    response = render(request, "advertisementAdd.html", context)
    response.set_cookie('sort', sort_for_paginator)
    response.set_cookie('date', state_sort_by_date)
    response.set_cookie('sorted_by', order_by)
    response.set_cookie('view_type', view_type)

    return response


def get_page_place_an_ad(request):
    category_list = Category.objects.filter(level__lte=1)
    oblast = Region.objects.filter(level=0)
    categories = Category.objects.filter(level=0)

    context = {
        "category_list": category_list,
        'adaptive_navigation': "Добавление объявления",
        'oblast': oblast,
        'categories': categories,
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


def get_advertisement_details_page(request, slug):
    '''Отдаем страничку с детальным описанием объявления'''
    advertisement_main = get_object_or_404(Advertisement.objects.prefetch_related("photoadvertisement_set"), slug=slug)
    Advertisement.objects.filter(id=advertisement_main.id).update(counter_views=F("counter_views")+1)
    category_crumbs = advertisement_main.category.get_ancestors(ascending=False, include_self=True)
    date = datetime.now(tz=get_current_timezone()) - timedelta(days=50)
    similar_advertisement = Advertisement.objects.filter(moderated=True,
                                                         is_active=True,
                                                         category_id=advertisement_main.category,
                                                         date_of_create__date__gte=date
                                                         ).exclude(id=advertisement_main.id).values('id')

    similar_advertisement = list(similar_advertisement)
    similar_advertisement = random.sample(similar_advertisement, 4 if len(similar_advertisement) >= 4 else len(similar_advertisement))
    print(similar_advertisement)
    similar_advertisement = Advertisement.objects.filter(id__in=[value.get('id') for value in similar_advertisement])
    context = {
        "advertisement": advertisement_main,
        "category_crumbs": category_crumbs,
        "similar_advertisement": similar_advertisement
    }
    return render(request=request,
                  template_name='advertisement_details.html',
                  context=context)


def editing_an_ad(request, id):
    advertisement = Advertisement.objects.get(id=id)

    region = Region.objects.all()
    oblast = region.filter(level=0)
    selected_oblast = region.get(id=advertisement.region.parent_id)
    cities = advertisement.region.get_siblings(include_self=True)
    family_categories = advertisement.category.get_family()

    list_categories = [category.get_siblings(include_self=True) for category in family_categories]
    categories = {key: value for key, value in zip(family_categories, list_categories)}

    additional_information = advertisement.category.field_set.all().prefetch_related("spisok")

    additional_values = {key: value for key, value in zip(advertisement.additional_information.keys(), map(lambda i: i.split(", "), advertisement.additional_information.values()))}

    additional_values_two = {}
    for i in additional_values.items():
        if len(i[1]) > 1:
            additional_values_two[i[0]] = [i[1][0], ElementTwo.objects.filter(element__title=i[1][0])]
    for i in additional_information:
        if i.min_val_interval_date:
            additional_values_two[i.title] = [str(date) for date in range(i.min_val_interval_date, i.max_val_interval_date + 1)]


    context = {
        'advertisement': advertisement,
        'oblast': oblast,
        'selected_oblast': selected_oblast,
        'cities': cities,
        'categories': categories,
        'additional_information': additional_information,
        'additional_values': additional_values,
        'additional_values_two': additional_values_two,
    }
    return render(request, 'editing_an_ad.html', context)


def search_result(request):
    search_parameters = {}
    search_parameters_only = {}
    key_delete = ['page', 'sort', 'date', 'price', 'text_search']
    cop = dict.copy(request.GET)

    sort_for_paginator = sorted_by_number(request.COOKIES.get('sort'))
    order_by = sorted_by(request.COOKIES.get('sorted_by'))
    state_sort_by_date = request.COOKIES.get('date', 0)
    category, category_bread_crumbs = where_to_look(cop.pop('category', None), Category)
    region, region_bread_crumbs = where_to_look(cop.pop('region', None), Region)

    if request.GET.get('date') or request.GET.get('price'):
        state_sort_by_date, order_by = sorted_by_date_or_price(request.GET)
    if request.GET.get('sort'):
        sort_for_paginator = sorted_by_number(request.GET.get('sort'))

    if category:
        search_parameters['category__in'] = category
    if region:
        search_parameters['region__in'] = region
    if request.GET.get('only_photo'):
        search_parameters_only['preview_image__exact'] = ''
        cop.pop('only_photo')
    if request.GET.get('only_video'):
        search_parameters_only['video_link__exact'] = ''
        cop.pop('only_video')
    if request.GET.get('only_title') and request.GET.get('text_search'):
        search_parameters['search_title_vector'] = request.GET.get('text_search')
        cop.pop('only_title')
    elif request.GET.get('text_search'):
        search_parameters['search_vector'] = request.GET.get('text_search')

    query = request.META.get('QUERY_STRING')
    for key in key_delete:
        cop.pop(key, None)
        query = query.replace(f'{key}={request.GET.get(key)}&', '')

    try:
        fields = Field.objects.filter(id__in=cop.keys())
    except ValueError:
        raise Http404()

    search, search_kt = search_additional_information(fields, cop)
    search_q, search_annotate = annotating_field(search_kt)

    if search:
        search_parameters['additional_information__contains'] = search
    if search_q:
        search_parameters['search_q'] = search_q

    advertisement_queryset1 = Advertisement.objects.annotate(**{key: KT(value) for key, value in search_annotate.items()}).filter(**search_parameters).exclude(**search_parameters_only).select_related('category', 'region').order_by("-raise_in_search", order_by)

    page_obj = variables_for_paginator(advertisement_queryset1,
                                       request.GET.get('page'),
                                       sort_for_paginator)

    context = {
        "ads_found": advertisement_queryset1.count(),
        "page_obj": page_obj,
        "region_bread_crumbs": region_bread_crumbs,
        "category_bread_crumbs": category_bread_crumbs,
        "query": query,
        'date': state_sort_by_date,
    }
    response = render(request, "searchResult.html", context)
    response.set_cookie('sort', sort_for_paginator)
    response.set_cookie('date', state_sort_by_date)
    response.set_cookie('sorted_by', order_by)

    return response