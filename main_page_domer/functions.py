from main_page_domer.models import Publication


def views_counter_publication(publication_id):
    data = Publication.objects.get(id=publication_id)
    data.counter_views += 1
    data.save()
