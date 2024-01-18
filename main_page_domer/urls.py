from django.urls import path

from main_page_domer.views import *

urlpatterns = [
    path('', get_main_page, name='home'),
    path('help/', get_help_page, name='help'),
    path('pa/', get_personal_account_page, name='pa'),
    path('ud/', get_user_data_page, name='ud'),
    path('in/', get_incoming_page, name='in'),
    path('out/', get_outgiong_page, name='out'),
    path('sent/', get_sent_page, name='sent'),
    path('adm_me/', get_admin_message_page, name='adm_me'),

]
