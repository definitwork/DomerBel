from django.urls import path

from api_domer.views import get_list_of_cities, get_list_of_categories

urlpatterns = [
    path('add_store/city/<int:id>', get_list_of_cities, name='list_of_cities'),
    path('add_store/categories/', get_list_of_categories, name='list_of_categories'),
]