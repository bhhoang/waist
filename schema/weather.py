"""
# schema/weather.py
# This module defines the schema for weather data.
"""

from typing import Optional
from pydantic import BaseModel, Field


class WeatherData(BaseModel):
    """
    Weather data schema for API requests and responses.
    """

    temp: float = Field(
        ..., description="Current temperature in degrees Celsius"
    )
    humidity: float = Field(
        ..., description="Current humidity percentage"
    )
    wind_speed: float = Field(
        ..., description="Current wind speed in km/h"
    )
    condition: str = Field(
        ...,
        description="Current weather condition \
                                            (e.g., sunny, rainy, cloudy)",
    )
    date: str = Field(
        ..., description="Date of the weather data in ISO 8601 format"
    )
    triggered_user: Optional[str] = Field(
        None, description="User who triggered the weather data retrieval"
    )
    api_source: Optional[str] = Field(
        None, description="Source of the weather data API"
    )
    loc_id: Optional[int] = Field(
        None, description="Location ID associated with the weather data"
    )

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "temp": 22.5,
                "humidity": 60,
                "wind_speed": 15.0,
                "condition": "Sunny",
                "triggered_user": "john_doe",
                "api_source": "Open-Meteo",
                "loc_id": 1,
                "date": "2023-10-01T12:00:00Z",
            }
        },
    }
