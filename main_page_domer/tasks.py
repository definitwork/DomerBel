import pytz
from celery import shared_task
from django.utils import timezone
from datetime import datetime

from advertisement.models import Advertisement


@shared_task()
def deactivate_advertisement():
    """ Функция деактивации объявлений по истечению времени публикации """
    # Получаем текущую дату и время с информацией о часовом поясе
    current_datetime = timezone.now()

    # Преобразуем текущую дату и время в часовой пояс, который вам нужен
    timezone1 = pytz.timezone("Europe/Minsk")
    aware_datetime = current_datetime.astimezone(timezone1)

    deactivate_advertisements = Advertisement.objects.filter(date_of_deactivate__lt=aware_datetime, is_active=True)
    print(deactivate_advertisements)
    deactivate_advertisements.update(is_active=False)


@shared_task()
def delete_advertisement():
    """ Функция удаления объявлений по истечению времени """
    # Получаем текущую дату и время с информацией о часовом поясе
    current_datetime = timezone.now()

    # Преобразуем текущую дату и время в часовой пояс, который вам нужен
    timezone1 = pytz.timezone("Europe/Minsk")
    aware_datetime = current_datetime.astimezone(timezone1)

    delete_advertisements = Advertisement.objects.filter(date_of_deactivate__lt=aware_datetime, is_active=True)
    print(delete_advertisements)
    delete_advertisements.delete()
