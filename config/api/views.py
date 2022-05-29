from rest_framework.decorators import api_view
from rest_framework.response import Response

from serialaizer import WeatherSerializer


@api_view(['GET'])
def weather_index(request):
    pass