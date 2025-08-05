"""
# schema/location.py
# This module defines the schema for location data.
"""
from pydantic import BaseModel, Field

class LocationData(BaseModel):
    """
    Location data schema for API requests and responses.
    """
    id: int = Field(..., description="The unique identifier for the location.")
    name: str = Field(..., description="The name of the location.")
    lat: float = Field(..., description="The latitude of the location.")
    long: float = Field(..., description="The longitude of the location.")
    country: str = Field(..., description="The country of the location.")

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "name": "Berlin",
                "latitude": 52.52,
                "longitude": 13.41,
                "country": "Germany"
            }
        }
    }
