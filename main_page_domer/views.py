from django.core.paginator import Paginator
from django.shortcuts import render

from advertisement.models import Advertisement, Region, Category, Store
from advertisement.utils import get_region_variables


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
                                                           extra_filters={"region__in": region_filter['region__in']})
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


def get_help_page(request):
    category_list = Category.objects.filter(level__lte=1)
    context = {
        "category_list": category_list
    }
    return render(request, 'help.html', context)
