"""
# model/weather.py
# This module defines the Weather model for the weather application.
"""

from datetime import datetime
from typing import Optional
from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Date,
    DateTime,
    ForeignKey,
    CheckConstraint,
)
from sqlalchemy.orm import relationship
from .db import Base


class Weather(Base):
    """
    Weather model represents weather data for a specific location and date.
    """

    __tablename__ = "weather"
    __table_args__ = (
        CheckConstraint("temp >= -100 AND temp <= 100", name="valid_temperature"),
        CheckConstraint("humidity >= 0 AND humidity <= 100", name="valid_humidity"),
        CheckConstraint("wind_speed >= 0", name="valid_wind_speed"),
    )

    id = Column(Integer, primary_key=True, index=True)
    loc_id = Column(
        Integer, ForeignKey("location.id", ondelete="CASCADE"), nullable=False
    )
    date = Column(Date, nullable=False)
    temp = Column(Float, nullable=False)
    condition = Column(String, nullable=False)
    wind_speed = Column(Float)
    humidity = Column(Integer)
    triggered_user = Column(String, nullable=True)
    api_source = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    location = relationship("Location", back_populates="weather")

    def save(self, db):
        """
        Save the weather record to the database.
        """
        db.add(self)
        db.commit()
        db.refresh(self)
        return self

    def update(self, db, **kwargs):
        """
        Update the weather record with provided fields.
        """
        for key, value in kwargs.items():
            if hasattr(self, key) and value is not None:
                setattr(self, key, value)
        db.commit()
        db.refresh(self)
        return self

    def delete(self, db):
        """
        Delete the weather record from the database.
        """
        db.delete(self)
        db.commit()
        return {"message": "Weather record deleted successfully"}

    @classmethod
    def get_by_location_and_date(
        cls, db, loc_id: int, date_param: str
    ) -> Optional["Weather"]:
        """
        Fetch a weather record by location ID and date.

        Args:
            db: Database session
            loc_id: Location ID
            date_param: string representation of the date (YYYY-MM-DD)
        """
        return (
            db.query(cls).filter(cls.loc_id == loc_id, cls.date == date_param).first()
        )

    @classmethod
    def get_by_location(cls, db, loc_id: int, limit: int = 10):
        """
        Fetch recent weather records for a location.
        """
        return (
            db.query(cls)
            .filter(cls.loc_id == loc_id)
            .order_by(cls.date.desc())
            .limit(limit)
            .all()
        )

    def to_dict(self):
        """
        Convert the weather record to a dictionary.
        """
        return {
            "id": self.id,
            "loc_id": self.loc_id,
            "date": self.date.isoformat() if self.date else None,
            "temp": self.temp,
            "condition": self.condition,
            "wind_speed": self.wind_speed,
            "humidity": self.humidity,
            "triggered_user": self.triggered_user,
            "api_source": self.api_source,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    @classmethod
    def get_from_date_range(
        cls, db, loc_id: int, start_date: str, end_date: str
    ):
        """
        Fetch weather records for a location within a date range.
        """
        return (
            db.query(cls)
            .filter(
                cls.loc_id == loc_id,
                cls.date >= start_date,
                cls.date <= end_date,
            )
            .order_by(cls.date.desc())
            .all()
        )

    def get_from_user(self, db, user: str):
        """
        Fetch weather records triggered by a specific user.
        """
        return (
            db.query(self)
            .filter(self.triggered_user == user)
            .order_by(self.date.desc())
            .all()
        )

    def __repr__(self):
        return (
            f"Weather(id={self.id}, loc_id={self.loc_id}, "
            f"date={self.date}, temp={self.temp}, "
            f"condition='{self.condition}')"
        )
