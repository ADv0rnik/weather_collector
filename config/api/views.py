from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.serializer import WeatherSerializer
from collector.models import Weather


@api_view(['GET'])
def weather_index(request):
    weather = Weather.objects.all()
    serializer = WeatherSerializer(weather, many=True)
    return Response(serializer.data)
