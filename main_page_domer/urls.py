from django.urls import path

from main_page_domer.views import *

urlpatterns = [
    path('', get_main_page, name='home'),
    path('help/', get_help_page, name='help'),
    path('personal_account/', get_personal_account_page, name='personal_account'),
    path('user_data/', get_user_data_page, name='user_data'),
    path('incoming_messages/', get_incoming_page, name='incoming_messages'),
    path('outgoing_messages/', get_outgoing_page, name='outgoing_messages'),
    path('sent_messages/', get_sent_page, name='sent_messages'),
    path('admin_messages/', get_admin_message_page, name='admin_messages'),
    path('add_store/', add_store, name='add_store'),
    path('add_store/city/<int:id>', get_list_of_cities, name='list_of_cities'),
    path('add_store/categories/', get_list_of_categories, name='list_of_categories'),
]
