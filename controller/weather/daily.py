"""
# controller/weather/daily.py
# This module fetches daily weather forecast data using the Open-Meteo API
"""

from datetime import datetime
import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry
from utils import convert_weather_code

cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

URL = "https://api.open-meteo.com/v1/forecast"


def get_daily_forecast(
    latitude: float,
    longitude: float,
    start_date: str = datetime.now().strftime("%Y-%m-%d"),
    end_date: str = (datetime.now() + pd.Timedelta(days=7)).strftime("%Y-%m-%d"),
) -> dict:
    """
    Fetch daily weather forecast for given latitude and longitude.
    """
    daily: str = ",".join(
        [
            "weather_code",
            "apparent_temperature_max",
            "sunshine_duration",
            "temperature_2m_max",
            "cloud_cover_mean",
            "relative_humidity_2m_mean",
            "pressure_msl_mean",
            "visibility_mean",
            "wind_speed_10m_mean",
            "temperature_2m_min",
        ]
    )

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": daily,
        "timezone": "auto",
        "start_date": start_date,
        "end_date": end_date,
    }
    responses = openmeteo.weather_api(URL, params=params)
    response = responses[0]

    time_range = pd.date_range(
        start=pd.to_datetime(response.Daily().Time(), unit="s", utc=True),
        end=pd.to_datetime(response.Daily().TimeEnd(), unit="s", utc=True),
        freq=pd.Timedelta(seconds=response.Daily().Interval()),
        inclusive="left",
    )

    daily_time_str = [time.isoformat() for time in time_range]

    weather_conditions = []

    for code in response.Daily().Variables(0).ValuesAsNumpy().tolist():
        weather_conditions.append(convert_weather_code(code))

    return {
        "daily_time": daily_time_str,
        "utc_offset_seconds": response.UtcOffsetSeconds(),
        "latitude": response.Latitude(),
        "longitude": response.Longitude(),
        "elevation": response.Elevation(),
        "daily_conditions": weather_conditions,
        "apparent_temperature_max": response.Daily()
        .Variables(1)
        .ValuesAsNumpy()
        .tolist(),
        "sunshine_duration": response.Daily().Variables(2).ValuesAsNumpy().tolist(),
        "temperature_2m_max": response.Daily().Variables(3).ValuesAsNumpy().tolist(),
        "cloud_cover_mean": response.Daily().Variables(4).ValuesAsNumpy().tolist(),
        "relative_humidity_2m_mean": response.Daily()
        .Variables(5)
        .ValuesAsNumpy()
        .tolist(),
        "pressure_msl_mean": response.Daily().Variables(6).ValuesAsNumpy().tolist(),
        "visibility_mean": response.Daily().Variables(7).ValuesAsNumpy().tolist(),
        "wind_speed_10m_mean": response.Daily().Variables(8).ValuesAsNumpy().tolist(),
        "temperature_2m_min": response.Daily().Variables(9).ValuesAsNumpy().tolist(),
    }
