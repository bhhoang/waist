"""
# geodata.py
# This module return geodata using open-meteo geocoding API
"""
import requests
from utils import fprint
from model.location import Location
from model.db import get_db

URL = "https://geocoding-api.open-meteo.com/v1/search"

def get_geodata(
    name: str, count: int = 1, language: str = "en", res_format: str = "json"
) -> dict:
    """
    Fetch geodata for a given location name, saves the result to database if not found
    """
    location = Location(name=name)
    db = next(get_db())
    existing_location = location.get_by_name(db, name)
    if existing_location:
        fprint(f"Location {name} already exists in the database.", level="info")
        return existing_location.to_dict()

    params = {"name": name, "count": count, "language": language, "format": res_format}
    response = requests.get(URL, params=params, timeout=10)
    if response.status_code != 200:
        fprint(f"Error: {response.status_code} - {response.text}", level="error")
        raise ValueError(f"Failed to fetch geodata for {name}")
    fprint(f"Data: {response.json()['results']}", level="info")
    data = response.json().get("results", [])
    if not data:
        fprint(f"No geodata found for {name}", level="warn")
        return {}
    location_data = data[0]
    location.lat = location_data.get("latitude")
    location.long = location_data.get("longitude")
    location.name = location_data.get("name")
    location.country = location_data.get("country")

    location.save(db)
    fprint(f"Location {name} saved to the database.", level="info")
    return location.to_dict()

def get_geodata_by_id(loc_id: int) -> dict:
    """
    Fetch geodata by location ID.
    """
    db = next(get_db())
    location = Location.get_by_id(db, loc_id)
    if not location:
        fprint(f"Location with ID {loc_id} not found.", level="error")
        return {}
    db.close()
    return location.to_dict()
