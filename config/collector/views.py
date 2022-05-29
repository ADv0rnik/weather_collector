from django.shortcuts import HttpResponse

from collector import tasks
from collector.models import Weather


def index(request):
    #tasks.get_weather_data.delay()
#    tasks.get_weather_data.apply_async(link=tasks.save_data.s())
    return HttpResponse('<h1>Loading data...</h1>')
