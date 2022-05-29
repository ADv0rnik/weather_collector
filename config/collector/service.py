import requests
import math

from decouple import config

from .models import Weather


REGIONS = [
    'Aktsyabrski',
    'Brahin',
    'Vyetka',
    'Gomel',
    'Dobrush',
    'Mazyr',
    'Khoyniki',
    'Loyew',
    'Rahachow',
    'Rechytsa',
    'Chachersk',
]


def get_data():
    key = config('API_KEY')
    api_url = 'https://api.openweathermap.org/data/2.5/find?q={}&appid=' + key + '&units=metric'
    data = []
    for region in REGIONS:
        data.append(requests.get(api_url.format(region)).json())
    cleaned_data = transform_weather(data)
    print(cleaned_data)
    return cleaned_data


def update_weather(data):
    for inst in data:
        weather = Weather.objects.create(
            region=inst['region'],
            temp=inst['temp'],
            hum=inst['hum'],
            rain=inst['rain'],
            fire_hazard_index_daily=inst['fire_hazard_index_daily'],
        )
        weather.save()


def transform_weather(data_list):
    weather_list = list()
    for data in data_list:
        temp = data.get('list')[0].get('main').get('temp')
        hum = data.get('list')[0].get('main').get('humidity')
        rain = is_rain(data)
        weather_dict = {
            'region': data.get('list')[0].get('name'),
            'temp': temp,
            'hum': hum,
            'rain': rain,
            'fire_hazard_index_daily': calculate_daily_index(
                temp=temp,
                hum=hum,
                rain=rain
            ),
        }
        weather_list.append(weather_dict)
    return weather_list


def is_rain(data):
    rain = 0.0
    if data.get('list')[0].get('rain') is None:
        return rain
    return data.get('list')[0].get('rain').get('1h', 0.0)


def calculate_daily_index(temp, hum, rain):
    """Calculate daily fire hazard index using specific equations

    Parameters
    ----------
    a, b - const coefficients to calculate dew point value
    dew_point - a required parameter to calculate hazard index

    Returns
    ----------
    int
        daily fire hazard index
    """
    a = 17.27
    b = 237.7
    tmp = (a*temp) / (b + temp) + math.log(hum / 100)
    dew_point = (b*tmp) / (a - tmp)
    if rain >= 5:
        return int(((temp - dew_point)*temp)*0.1)
    return int((temp - dew_point)*temp)
