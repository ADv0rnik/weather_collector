from rest_framework import viewsets

from api.serializer import WeatherSerializer
from collector.models import Weather


class WeatherViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Weather.objects.all()
    serializer_class = WeatherSerializer
