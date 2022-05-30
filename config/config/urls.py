from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('collector.urls')),
    path('weather/', include('api.urls')),
]
