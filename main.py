"""
# main.py
# This module initializes the FastAPI application and includes the routers.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from router import location_router, weather_router
from router.export_router import router as export_router
from model.db import create_tables

# Metadata
app = FastAPI(
    title="Weather API",
    description="An API to get weather data and manage weather records.",
    version="1.0.0",
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(location_router.router, tags=["location"])
app.include_router(weather_router.router, tags=["weather"])
app.include_router(export_router, tags=["export"])

@app.get("/")
async def root():
    """
    Root endpoint to check if the API is running.
    """
    return {"message": "Welcome to the Weather API"}

def main():
    """
    Main function to run the FastAPI application.
    It creates the database tables and starts the Uvicorn server.
    """
    create_tables()
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

if __name__ == "__main__":
    main()
