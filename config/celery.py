import os
from datetime import timedelta
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
app = Celery("config")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

'''плановые задачи'''
app.conf.beat_schedule = {
    "deactivate_advertisement": {
        "task": 'main_page_domer.tasks.deactivate_advertisement',
        # "schedule": timedelta(seconds=10)
        "schedule": crontab(hour=2, minute=27)
    },
    "delete_advertisement": {
        "task": 'main_page_domer.tasks.delete_advertisement',
        "schedule": timedelta(seconds=10)
        # "schedule": crontab(hour=2, minute=27)
    },
}

if __name__ == '__main__':
    app.start()
