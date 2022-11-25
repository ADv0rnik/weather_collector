from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from api.serializer import WeatherSerializer
from collector.models import Weather


class WeatherViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = WeatherSerializer
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        queryset = Weather.objects.all()
        region = self.request.query_params.get('region')
        print(region)
        if region:
            queryset = Weather.objects.filter(region=region)
        return queryset

