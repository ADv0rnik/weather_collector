from django.db import models


class Weather(models.Model):
    region = models.CharField(max_length=50)
    temp = models.FloatField(blank=False)
    hum = models.IntegerField(blank=False)
    rain = models.FloatField(blank=False)
    date_created = models.DateTimeField(auto_now_add=True)
    fire_hazard_index_daily = models.FloatField(blank=True, default=100.0)

    def __str__(self):
        return f"{self.region} {self.date_created}"

    class Meta:
        verbose_name_plural = 'Weather data'
