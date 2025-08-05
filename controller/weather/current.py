"""
# controller/weather/current.py
# This module fetches current weather data using the Open-Meteo API.
"""
import openmeteo_requests
import requests_cache
from retry_requests import retry
from utils import convert_weather_code

cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

URL = "https://api.open-meteo.com/v1/forecast"

def get_current_weather(
    latitude: float,
    longitude: float,
    current: str = ",".join(
        [
            "apparent_temperature",
            "relative_humidity_2m",
            "temperature_2m",
            "is_day",
            "cloud_cover",
            "weather_code",
            "pressure_msl",
            "wind_speed_10m",
        ]
    ),
) -> dict:
    """
    Fetch current weather for given latitude and longitude.
    """
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": current,
        "timezone": "auto",
    }
    responses = openmeteo.weather_api(URL, params=params)
    response = responses[0]
    var_list = current.split(",")
    result = {}
    for i, name in enumerate(var_list):
        value = response.Current().Variables(i).Value()
        result[name.strip()] = value
        if name.strip() == "weather_code":
            result["weather_condition"] = convert_weather_code(value)
    print(result)
    return result
