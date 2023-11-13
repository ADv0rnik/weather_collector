from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from api.views import WeatherViewSet


router = routers.SimpleRouter()
router.register(r'weather', WeatherViewSet, basename='weather')

print(router.urls)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('collector.urls')),
    path('api/v1/', include(router.urls)),
]
