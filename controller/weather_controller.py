"""
# weather.py
# This module fetches weather data using the Open-Meteo API
"""

import sys
import os
import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    from .weather.current import get_current_weather
    from .weather.daily import get_daily_forecast
    from .weather.hourly import get_hourly_forecast
except ImportError:
    from controller.weather.current import get_current_weather
    from controller.weather.daily import get_daily_forecast
    from controller.weather.hourly import get_hourly_forecast

cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)


URL = "https://api.open-meteo.com/v1/forecast"


def export_csv(data: dict, filename: str) -> None:
    """
    Export weather data to a CSV file.

    Args:
        data (dict): Weather data to export.
        filename (str): Name of the output CSV file.
    """
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Data exported to {filename}")

if __name__ == "__main__":
    LAT = 52.52
    LONG = 13.419998
    daily_data = get_daily_forecast(LAT, LONG)
    current_data = get_current_weather(LAT, LONG)
    hourly_data = get_hourly_forecast(LAT, LONG)
    print("Daily Data:")
    print(daily_data)
    print("Current Data:")
    print(current_data)
    print("Hourly Data:")
    print(hourly_data)
