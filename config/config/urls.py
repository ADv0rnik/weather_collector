from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from api.views import WeatherViewSet


router = routers.SimpleRouter()
router.register(r'weather', WeatherViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('collector.urls')),
    path('api/', include(router.urls)),
]
