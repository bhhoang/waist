"""
# model/location.py
# This module defines the Location model for the weather application.
# It represents a geographical location with attributes like name, latitude, and longitude.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, CheckConstraint
from sqlalchemy.orm import relationship
from .db import Base


class Location(Base):
    """
    Location model represents a geographical location with its attributes.
    It includes a unique identifier, name, latitude, longitude, and creation timestamp.
    """

    __tablename__ = "location"

    __table_args__ = (
        CheckConstraint("lat >= -90 AND lat <= 90", name="valid_latitude"),
        CheckConstraint(
            "long >= -180 AND long <= 180", name="valid_longitude"
        ),
    )

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    lat = Column(Float, nullable=False)
    long = Column(Float, nullable=False)
    country = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    weather = relationship(
        "Weather", back_populates="location", cascade="all, delete-orphan"
    )

    def save(self, db):
        """
        Save the location to the database.
        """
        db.add(self)
        db.commit()
        db.refresh(self)
        return self

    @classmethod
    def get_by_name(cls, db, name):
        """
        Fetch the location by name from the database.
        """
        return db.query(cls).filter(cls.name.ilike(name)).first()

    def to_dict(self):
        """
        Convert the location object to a dictionary.
        """
        return {
            "id": self.id,
            "name": self.name,
            "lat": self.lat,
            "long": self.long,
            "country": self.country,
            "created_at": self.created_at.isoformat(),
        }

    def __repr__(self):
        return (
            f"Location(id={self.id}, name='{self.name}', "
            f"lat={self.lat}, long={self.long}, "
            f"country='{self.country}', created_at={self.created_at})"
        )
