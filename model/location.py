"""
# model/location.py
# This module defines the Location model for the weather application.
# It represents a geographical location with attributes like name, latitude, and longitude.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from .db import Base

class Location(Base):
    """
    Location model represents a geographical location with its attributes.
    It includes a unique identifier, name, latitude, longitude, and creation timestamp.
    """
    __tablename__ = "location"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    weather = relationship("Weather", back_populates="location", cascade="all, delete-orphan")

    def __repr__(self):
        return f"Location(id={self.id}, name='{self.name}', lat={self.lat}, lon={self.lon})"
