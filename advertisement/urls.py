from django.urls import path

from .views import get_advertisement_page, get_advertisement_by_category

urlpatterns = [
    path('', get_advertisement_page, name='advertisement'),
    path('advertisement_by_category/<slug:category_slug>/', get_advertisement_by_category, name='advertisement_by_category'),
]
