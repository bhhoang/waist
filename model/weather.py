"""
# model/Weather.py
# This module defines the Weather model for the weather application.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .db import Base

class WeatherRecord(Base):
    """
    WeatherRecord model represents weather data for a specific location and date.
    """

    __tablename__ = "weather"

    id = Column(Integer, primary_key=True, index=True)
    loc_id = Column(
        Integer, ForeignKey("location.id", ondelete="CASCADE"), nullable=False
    )
    date = Column(Date, nullable=False)
    temp = Column(Float, nullable=False)
    condition = Column(String, nullable=False)
    wind_speed = Column(Float)
    hum = Column(Integer)
    api_source = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now)

    location = relationship("Location", back_populates="weather")

    def __repr__(self):
        return f"Weather(id={self.id}, \
                loc_id={self.loc_id}, \
                date={self.date}, \
                temp={self.temp}, \
                condition='{self.condition}')"
