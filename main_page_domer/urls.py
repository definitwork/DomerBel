from django.urls import path

from main_page_domer.views import *

urlpatterns = [
    path('', get_main_page, name='home'),
    path('stores/', get_stores_page, name='stores'),
    # path('stores/<slug:store_slug>/', get_store_by_category, name='store_by_category'),
    path('help/', get_help_page, name='help'),
]
