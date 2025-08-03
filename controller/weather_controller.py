"""
# weather.py
# This module fetches weather data using the Open-Meteo API
"""
import openmeteo_requests

import pandas as pd
import requests_cache
from retry_requests import retry

from utils import fprint

cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

URL = "https://api.open-meteo.com/v1/forecast"


def get_weather_data(
    latitude: float,
    longitude: float,
    daily: str = ",".join(
        [
            "temperature_2m",
            "apparent_temperature",
            "relative_humidity_2m",
            "dew_point_2m",
            "uv_index",
            "uv_index_clear_sky",
            "wind_speed_10m",
            "wind_direction_10m",
            "wind_gusts_10m",
            "cloud_cover",
            "visibility",
            "surface_pressure",
        ]
    ),
    timezone: str = "auto",
) -> dict:
    """
    Fetch weather data for given latitude and longitude.
    """
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": daily,
        "timezone": timezone,
    }
    responses = openmeteo.weather_api(URL, params=params)
    response = responses[0]

    return {
        "latitude": response.Latitude(),
        "longitude": response.Longitude(),
        "elevation": response.Elevation(),
        "utc_offset_seconds": response.UtcOffsetSeconds(),
        "hourly_data": response.Hourly().Variables(0).ValuesAsNumpy().tolist(),
    }

def export_csv(data: dict, filename: str) -> None:
    """
    Export weather data to a CSV file.
    
    Args:
        data (dict): Weather data to export.
        filename (str): Name of the output CSV file.
    """
    hourly_data = {
        "date": pd.date_range(
            start=pd.to_datetime(data["hourly_data"]["time"], unit="s", utc=True),
            end=pd.to_datetime(data["hourly_data"]["time_end"], unit="s", utc=True),
            freq=pd.Timedelta(seconds=data["hourly_data"]["interval"]),
            inclusive="left",
        ),
        "temperature_2m": data["hourly_data"]["temperature_2m"],
    }

    hourly_dataframe = pd.DataFrame(data=hourly_data)
    hourly_dataframe.to_csv(filename, index=False)
    fprint(f"Data exported to {filename}", level="info")
