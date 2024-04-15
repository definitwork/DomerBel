from django.urls import path

from api_domer.views import get_list_of_cities, get_list_of_categories, get_region_list, get_category_list, \
    get_categories_for_search, get_field_list, get_elementtwo_list, save_advertisement, get_store_for_advertisement

urlpatterns = [
    path('add_store/city/<int:id>', get_list_of_cities, name='list_of_cities'),
    path('add_store/categories/', get_list_of_categories, name='list_of_categories'),
    path('categories_for_search/<int:id>', get_categories_for_search, name='categories_for_search'),
    path('get_region_list/', get_region_list),
    path('get_category_list/', get_category_list),
    path('get_field_list/', get_field_list),
    path('get_elementtwo_list/', get_elementtwo_list),
    path('save_advertisement/', save_advertisement, name='save_advertisement'),
    path('get_store_for_advertisement/', get_store_for_advertisement, name='get_store_for_advertisement'),
]