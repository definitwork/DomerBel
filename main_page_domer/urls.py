from django.urls import path

from main_page_domer.views import *

urlpatterns = [
    path('', get_main_page, name='home'),
    path('help/', get_help_page, name='help'),
    path('user_data/', get_user_data_page, name='user_data'),
]
