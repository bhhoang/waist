"""
# routers/weather_router.py
# This module defines the API endpoints for weather data services.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from controller.weather_controller import (
    get_current_weather,
    get_daily_forecast,
    get_hourly_forecast,
)
from controller.location_controller import get_geodata
from schema.weather import WeatherData
from model.weather import Weather
from model.db import get_db
from utils import fprint, random_user_string

router = APIRouter(prefix="/weather")


# READ-ONLY ENDPOINTS
@router.get("/current")
async def current_weather_endpoint(name: str):
    """
    Endpoint to fetch current weather for a given location name.

    Args:
        name: The name of the city or location.

    Returns:
        WeatherData: The current weather data.
    """
    try:
        location = get_geodata(name)
        if not location:
            return {"error": 404, "detail": "Location not found"}

        res = get_current_weather(location["lat"], location["long"])
        res["latitude"] = location["lat"]
        res["longitude"] = location["long"]
        return res
    except HTTPException as e:
        return {"error": 400, "detail": str(e)}


@router.get("/daily")
async def daily_forecast_endpoint(name: str):
    """
    Endpoint to fetch daily weather forecast for a given location name.

    Args:
        name: The name of the city or location.

    Returns:
        list[WeatherData]: A list of daily weather forecasts.
    """
    try:
        location = get_geodata(name)
        if not location:
            return {"error": 404, "detail": "Location not found"}
        return get_daily_forecast(location["lat"], location["long"])
    except HTTPException as e:
        return {"error": 400, "detail": str(e)}


@router.get("/hourly")
async def hourly_forecast_endpoint(name: str):
    """
    Endpoint to fetch hourly weather forecast for a given location name.

    Args:
        name: The name of the city or location.

    Returns:
        list[WeatherData]: A list of hourly weather forecasts.
    """
    try:
        location = get_geodata(name)
        if not location:
            return {"error": 404, "detail": "Location not found"}
        return get_hourly_forecast(location["lat"], location["long"])
    except HTTPException as e:
        return {"error": 400, "detail": str(e)}

@router.get("/user")
async def get_user_weather_records(
    user: str = Query(None, description="Filter by user name"),
    db: Session = Depends(get_db)
):
    """
    Endpoint to get weather records filtered by user name.

    Args:
        user: The name of the user to filter records by.
        db: The database session dependency.

    Returns:
        list[WeatherData]: A list of weather records for the specified user.
    """
    if not user:
        raise HTTPException(status_code=400, detail="User name is required")

    records = db.query(Weather).filter(Weather.triggered_user == user).all()
    if not records:
        raise HTTPException(status_code=404, detail="No records found for this user")

    return [record for record in records]

# CREATE ENDPOINT
@router.post("/create")
async def create_weather_record(
    weather: WeatherData,
    db: Session = Depends(get_db)
    ):
    """
    Endpoint to create a new current weather record in the database.

    Args:
        weather: The weather data to be stored.
        db: The database session dependency.

    Returns:
        WeatherData: The created weather record.
    """
    weather_data = Weather(**weather.model_dump())
    try:
        created_record = weather_data.save(db)
        return {"message": "Weather record created successfully",}
    except HTTPException as e:
        return {"error": 500, "detail": f"Database error: {str(e)}"}



@router.get("/{weather_id}", response_model=WeatherData)
async def get_weather_record(weather_id: int, db: Session = Depends(get_db)):
    """
    Endpoint to get a specific weather record from the database.

    Args:
        weather_id: The ID of the weather record.
        db: The database session dependency.

    Returns:
        WeatherData: The requested weather record.
    """
    existing_weather = db.query(Weather).filter(Weather.id == weather_id).first()
    if not existing_weather:
        raise HTTPException(status_code=404, detail="Weather record not found")

    return WeatherData.model_validate(existing_weather)


@router.put("/{weather_id}", response_model=WeatherData)
async def update_weather_record(
    weather_id: int, weather: WeatherData, db: Session = Depends(get_db)
):
    """
    Endpoint to update an existing weather record.

    Args:
        weather_id: The ID of the weather record to update.
        weather: The new weather data.
        db: The database session dependency.

    Returns:
        WeatherData: The updated weather record.
    """
    existing_weather = db.query(Weather).filter(Weather.id == weather_id).first()
    if not existing_weather:
        raise HTTPException(status_code=404, detail="Weather record not found")

    try:
        updated_record = existing_weather.update(db, **weather.model_dump())
        return WeatherData.model_validate(updated_record)
    except HTTPException as e:
        return {"error": 500, "detail": f"Database error: {str(e)}"}


@router.delete("/{weather_id}")
async def delete_weather_record(weather_id: int, db: Session = Depends(get_db)):
    """
    Endpoint to delete a weather record.

    Args:
        weather_id: The ID of the weather record to delete.
        db: The database session dependency.

    Returns:
        dict: A success message.
    """
    existing_weather = db.query(Weather).filter(Weather.id == weather_id).first()
    if not existing_weather:
        return {"error": 404, "detail": "Weather record not found"}

    try:
        db.delete(existing_weather)
        db.commit()
        return {"message": "Weather record deleted successfully"}
    except HTTPException as e:
        db.rollback()
        return {"error": 500, "detail": f"Database error: {str(e)}"}
