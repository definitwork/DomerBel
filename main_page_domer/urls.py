from django.urls import path

from main_page_domer.views import get_main_page, get_help_page, get_personal_account_page

urlpatterns = [
    path('', get_main_page, name='home'),
    path('help/', get_help_page, name='help'),
    path('pa/', get_personal_account_page, name='pa'),

]
