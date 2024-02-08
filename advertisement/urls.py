from django.urls import path

from .views import get_advertisement_page, get_advertisement_by_category, load_new_region_to_model

urlpatterns = [
    path('bany/', load_new_region_to_model),
    path('', get_advertisement_page, name='advertisement'),
    path('<slug:category_slug>/', get_advertisement_by_category, name='advertisement_by_category'),

]
