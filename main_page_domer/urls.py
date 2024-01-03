from django.urls import path

from main_page_domer.views import get_main_page


urlpatterns = [
    path('', get_main_page)
]