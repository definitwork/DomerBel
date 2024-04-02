from django.urls import path

from .views import get_advertisement_page, get_advertisement_by_category, get_page_place_an_ad, \
    get_advertisement_details_page

urlpatterns = [
    path('', get_advertisement_page, name='advertisement'),

    path('advertisement/<slug:category_slug>/', get_advertisement_by_category, name='advertisement_by_category'),
    path('place_an_ad/', get_page_place_an_ad, name='place_an_ad'),
    path('advertisement_details/<int:id>/', get_advertisement_details_page, name='advertisement_details'),
]
