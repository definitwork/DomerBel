from django.urls import path

from main_page_domer.views import *

urlpatterns = [
    path('', get_main_page, name='home'),
    path('stores/', get_stores_page, name='stores'),
    path('stores/<slug:category_slug>/', get_stores_by_category, name='stores_by_category'),
    path('store/<slug:store_slug>/', get_store_by_title, name='store_by_title'),
    path('store/<slug:store_slug>/<slug:category_slug>/', get_store_by_title_and_category, name='store_by_title_and_category'),
    path('help/', get_help_page, name='help'),
]
