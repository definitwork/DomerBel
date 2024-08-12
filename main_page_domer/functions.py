import os
from datetime import datetime
from urllib.parse import urljoin

from django.core.files.storage import FileSystemStorage
from django.db.models import F

from config import settings
from main_page_domer.models import Publication


def views_counter_publication(publication_slug):
    Publication.objects.filter(slug=publication_slug).update(counter_views=F('counter_views')+1)


class CkeditorCustomStorage(FileSystemStorage):
    """Кастомное расположение для медиа файлов редактора CKEditor5"""

    def get_folder_name(self):
        return datetime.now().strftime('%Y/%m/%d')

    def get_valid_name(self, name):
        return name

    def _save(self, name, content):
        folder_name = self.get_folder_name()
        name = os.path.join(folder_name, self.get_valid_name(name))
        return super()._save(name, content)

    location = os.path.join(settings.MEDIA_ROOT, 'images/publications/')
    base_url = urljoin(settings.MEDIA_URL, 'images/publications/')
