import logging

from django.shortcuts import HttpResponse
from collector import tasks

logger = logging.getLogger('collector')


def index(request):
    tasks.get_weather_data.delay()
    logger.info("The application has been started")
    return HttpResponse('<h1>Loading data...</h1>')
