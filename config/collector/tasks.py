from config.celery import app

from collector.service import get_data, update_weather


@app.task(name="get-weather-data")
def get_weather_data():
    data = get_data()
    update_weather(data)
    return f"Success!"
