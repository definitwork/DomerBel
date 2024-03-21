from django.urls import path

from main_page_domer.views import *

urlpatterns = [
    path('', get_main_page, name='home'),
    path('stores/', get_stores_page, name='stores'),
    path('help/', get_help_page, name='help'),
]
