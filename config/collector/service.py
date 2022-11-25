import requests
import math
from decouple import config
from .models import Weather
from django_filters import rest_framework as filters


KEY = config('API_KEY')
DEFAULT_RAIN_VALUE = 0.0
DEFAULT_HAZARD_INDEX = 50
API_URL = 'https://api.openweathermap.org/data/2.5/find?q={}&appid=' + KEY + '&units=metric'
REGIONS = [
    'Aktsyabrski',
    'Brahin',
    'Buda-Kashalyova',
    'Chachersk',
    'Dobrush',
    'Gomel',
    'Vyetka',
    'Mazyr',
    'Karma',
    'Kalinkavichy',
    'Khoyniki',
    'Loyew',
    'Lelchytsy',
    'Narowlya',
    'Pyetrykaw',
    'Rahachow',
    'Rechytsa',
    'Svyetlahorsk',
    'Yelsk',
    'Zhlobin',
    'Zhytkavichy'
]


def get_data_from_api() -> dict:
    data = list()
    for region in REGIONS:
        weather_data = requests.get(API_URL.format(region))
        assert weather_data.status_code == 200
        data.append(weather_data.json())
    return get_clean_data(data)


def update_weather(data):
    for key, value in data.items():
        region = key,
        temp = value.get('temp'),
        hum = value.get('humidity'),
        rain = value.get('rain'),
        daily_index = value.get('daily_index')
        weather = Weather.objects.create(
            region=region[0],
            temp=temp[0],
            hum=hum[0],
            rain=rain[0],
            fire_hazard_index_daily=daily_index[0],
        )
        weather.save()


def get_clean_data(response: list) -> dict:
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
        data = item.get('list')[0]
        city = data.get('name')
        coord = data.get('coord')
        rain = get_rain(data)
        for key, value in data.items():
            if key == 'main':
                temp = value.get('temp')
                hum = value.get('humidity')
                daily_hazard_index = calculate_daily_index(temp=temp, humidity=hum, rain=rain),
                weather[city] = {
                    "coord": coord,
                    "temp": temp,
                    "humidity": hum,
                    "rain": rain,
                    "daily_index": daily_hazard_index,
                }
    return weather


def get_rain(data: dict) -> float:
    rain = data.get('rain')
    if not rain:
        return DEFAULT_RAIN_VALUE
    return rain.get('1h')


def calculate_daily_index(**kwargs):
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
        print(f"An error occurred {error}")
        return DEFAULT_HAZARD_INDEX
    else:
        if (rain := kwargs.get('rain')) >= 5:
            return int(((kwargs.get('temp') - dew_point) * kwargs.get('temp')) * 0.1)
        return round(float((kwargs.get('temp') - dew_point) * kwargs.get('temp')), 2)
