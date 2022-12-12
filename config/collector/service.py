import requests
import math
from decouple import config
from .models import Weather
from django_filters import rest_framework as filters
import logging


logger = logging.getLogger('collector')


class WeatherCollector:
    KEY = config('API_KEY')
    DEFAULT_RAIN_VALUE = 0.0
    DEFAULT_HAZARD_INDEX = 50
    API_URL = 'https://api.openweathermap.org/data/2.5/find?q={}&appid=' + KEY + '&units=metric'
    CITIES_ID_MAPPING = {'Aktsyabrski': 17, 'Brahin': 18, 'Buda-Kashalyova': 19, 'Chachersk': 20, 'Dobrush': 21,
                         "Homyel'": 22, 'Vyetka': 34, 'Mazyr': 28, 'Karma': 24, 'Kalinkavichy': 23,
                         'Khoyniki': 25, 'Loyew': 26, 'Lelchytsy': 27, 'Narowlya': 29, 'Pyetrykaw': 30,
                         'Rahachow': 31, 'Rechytsa': 32, 'Svyetlahorsk': 33, "Yel’sk": 35, 'Zhlobin': 36, 'Zhytkavichy': 37}

    def get_data_from_api(self) -> dict:
        data = list()
        for region in self.CITIES_ID_MAPPING.keys():
            weather_data = requests.get(self.API_URL.format(region))
            logger.info(f"GET: {self.API_URL.format(region)}")
            assert weather_data.status_code == 200
            data.append(weather_data.json())
        return self.clean_data(data)

    def clean_data(self, response: list) -> dict:
        """
        The method extract necessary data from api response and put it into JSON for further treatment

        Parameters
        ----------
        response
            list of dictionaries contained weather data

        Returns
        -------
        weather
            dictionary of temperature, humidity, precipitation and calculated hazard index for each predefined region
        """
        weather = dict()
        for item in response:
            print(item)
            if data := item.get('list', {})[0]:
                print(data)
                city = data.get('name')
                coord = data.get('coord')
                rain = self.get_rain(data)
                for key, value in data.items():
                    if key == 'main':
                        temp = value.get('temp')
                        hum = value.get('humidity')
                        daily_hazard_index = self.calculate_daily_index(temp=temp, humidity=hum, rain=rain),
                        weather[city] = {
                            "coord": coord,
                            "temp": temp,
                            "humidity": hum,
                            "rain": rain,
                            "daily_index": daily_hazard_index,
                        }
        return weather

    def update_weather(self, data):
        for key, value in data.items():
            region = key,
            temp = value.get('temp'),
            hum = value.get('humidity'),
            rain = value.get('rain'),
            daily_index = value.get('daily_index')
            weather = Weather.objects.create(
                region_id=self.generate_id(region[0]),
                region=region[0],
                temp=temp[0],
                hum=hum[0],
                rain=rain[0],
                fire_hazard_index_daily=daily_index[0],
            )
            weather.save()
            logger.info(f"Object {weather} has been created")

    def generate_id(self, region: str) -> int:
        return self.CITIES_ID_MAPPING.get(region)

    def get_rain(self, data: dict) -> float:
        rain = data.get('rain')
        if not rain:
            return self.DEFAULT_RAIN_VALUE
        return rain.get('1h')

    def calculate_daily_index(self, **kwargs):
        """
        Calculate daily fire hazard index using specific equations a, b, dew_point - const coefficients to calculate
        dew point value required parameter to calculate hazard index

        Parameters
        ----------
        kwargs
            temperature, humidity, precipitation

        Returns
        -------
        int
            calculated daily fire hazard index
        """
        a = 17.27
        b = 237.7
        try:
            tmp = (a * kwargs.get('temp')) / (b + kwargs.get('temp')) + math.log(kwargs.get('humidity') / 100)
            dew_point = (b * tmp) / (a - tmp)
        except ZeroDivisionError as error:
            logger.error(f"An error occurred {error}. Set HAZARD_INDEX to default")
            return self.DEFAULT_HAZARD_INDEX
        else:
            if (rain := kwargs.get('rain')) >= 5:
                return int(((kwargs.get('temp') - dew_point) * kwargs.get('temp')) * 0.1)
            return round(float((kwargs.get('temp') - dew_point) * kwargs.get('temp')), 2)


class WeatherFilter(filters.FilterSet):
    pass