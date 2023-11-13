import os

from django.conf import settings
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


app.conf.beat_schedule = {
    "get-daily-weather-data": {
        "task": "get-weather-data",
        "schedule": crontab(minute='*/1')
    },
}

