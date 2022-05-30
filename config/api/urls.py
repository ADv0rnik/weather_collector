from django.urls import path
from api.views import weather_index


urlpatterns = [
    path('', weather_index, name='weather_index')
]
