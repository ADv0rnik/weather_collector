from config.celery import app

from collector.service import WeatherCollector


@app.task(name="get-weather-data")
def get_weather_data():
    weather_collector = WeatherCollector()
    data = weather_collector.get_data_from_api()
    weather_collector.update_weather(data)
    return f"Success!"
