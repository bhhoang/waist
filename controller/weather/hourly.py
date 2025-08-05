"""
# controller/weather/hourly.py
# This module fetches hourly weather forecast data using the Open-Meteo API.
"""
import openmeteo_requests

import pandas as pd
import requests_cache
from retry_requests import retry

cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

URL = "https://api.open-meteo.com/v1/forecast"


def get_hourly_forecast(latitude: float, longitude: float) -> dict:
    """
    Fetch hourly weather forecast for given latitude and longitude.
    """
    hourly: str = ",".join(
        [
            "temperature_2m",
        ]
    )

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": hourly,
        "timezone": "auto",
    }
    responses = openmeteo.weather_api(URL, params=params)
    response = responses[0]

    time_range = pd.date_range(
        start=pd.to_datetime(response.Hourly().Time(), unit="s", utc=True),
        end=pd.to_datetime(response.Hourly().TimeEnd(), unit="s", utc=True),
        freq=pd.Timedelta(seconds=response.Hourly().Interval()),
        inclusive="left",
    )
    hourly_time_str = time_range.strftime("%Y-%m-%dT%H:%M:%S").tolist()

    data = {
        "temperature_2m": response.Hourly().Variables(0).ValuesAsNumpy().tolist(),
        "time": hourly_time_str,
    }

    return data
