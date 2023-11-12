import logging

from django.shortcuts import HttpResponse
from collector import tasks

logger = logging.getLogger('collector')


def index(request):
    tasks.get_weather_data.delay()
    logger.info("The application has been started")
#    tasks.get_weather_data.apply_async(link=tasks.save_data.s())
    return HttpResponse('<h1>Loading data...</h1>')
