[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3100/)

### Weather-collector
#### Aliaksanrd Dvornik (May 17, 2022)

The application allows to collect and process weather data in order to calculate Fire hazard index for forest fires in Gomel region (Belarus)

#### Usage
1. Clone repository with the following command
`git clone https://github.com/ADv0rnik/weather_collector.git`

2. Run `pip install -r requirements.txt` in your virtual environment 

3. Run `python manage.py runserver` command to run server on the local machine

4. The weather-collector is using Redis together with celery to manage async tasks. Run the following commands:
```commandline
docker run -d -p 6379:6379 redis

celery -A config worker -l info
```


