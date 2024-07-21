from django.db.models import F
from main_page_domer.models import Publication


def views_counter_publication(publication_slug):
    Publication.objects.filter(slug=publication_slug).update(counter_views=F('counter_views')+1)
