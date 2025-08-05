"""
# routers/location_router.py
# This module defines the API endpoints for location-related services.
"""
from fastapi import APIRouter, HTTPException
from controller.location_controller import get_geodata
from schema.location import LocationData

router = APIRouter(prefix="/geodata")

@router.get("", response_model=LocationData)
async def read_geodata_endpoint(name: str):
    """
    Endpoint to fetch geodata (latitude and longitude) for a given location name.
    
    Args:
        name: The name of the city or location.
        
    Returns:
        LocationData: The geodata for the specified location.
    """
    try:
        return get_geodata(name)
    except HTTPException as e:
        return {"error": 404, "detail": str(e)}
