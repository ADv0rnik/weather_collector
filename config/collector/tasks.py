from config.celery import app

from collector.service import get_data_from_api, update_weather


@app.task(name="get-weather-data")
def get_weather_data():
    data = get_data_from_api()
    update_weather(data)
    return f"Success!"
