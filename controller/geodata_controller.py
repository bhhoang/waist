"""
# geodata.py
# This module return geodata using open-meteo geocoding API
"""
import requests
from utils import fprint

URL = "https://geocoding-api.open-meteo.com/v1/search"


def get_geodata(
    name: str, count: int = 1, language: str = "en", res_format: str = "json"
) -> dict:
    """
    Fetch geodata for a given location name.
    """
    params = {"name": name, "count": count, "language": language, "format": res_format}
    response = requests.get(URL, params=params, timeout=10)
    if response.status_code != 200:
        fprint(f"Error: {response.status_code} - {response.text}", level="error")
        raise ValueError(f"Failed to fetch geodata for {name}")
    fprint(f"Data: {response.json()['results']}", level="info")
    return response.json()
