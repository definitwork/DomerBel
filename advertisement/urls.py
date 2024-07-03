from django.urls import path
from .views import get_advertisement_page, get_advertisement_by_category, get_page_place_an_ad, get_page_place_an_favorites, get_bulk_import_of_ads
from .views import get_advertisement_page, get_advertisement_by_category, get_page_place_an_ad, \
    get_advertisement_details_page, get_page_place_an_favorites,download_file_with_error_ads

urlpatterns = [
    path('', get_advertisement_page, name='advertisement'),
    path('advertisement/<slug:category_slug>/', get_advertisement_by_category, name='advertisement_by_category'),
    path('place_an_ad/', get_page_place_an_ad, name='place_an_ad'),
    path('favorites/', get_page_place_an_favorites, name='favorites'),
    path('import_bulk_of_ads/',get_bulk_import_of_ads),
    path('advertisement_details/<int:id>/', get_advertisement_details_page, name='advertisement_details'),
    path('download_file_with_error_ads/',download_file_with_error_ads)

]
