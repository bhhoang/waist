"""
# router/export_router.py
# This module defines the API endpoints for exporting data in various formats.
"""

import csv
import json
import xml.etree.ElementTree as ET
from datetime import datetime
from io import StringIO
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy.orm import Session

from model.db import get_db
from model.location import Location
from model.weather import Weather


router = APIRouter(prefix="/export")


def _get_all_data(
    db: Session,
    location: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    user: Optional[str] = None,
):
    """
    Helper function to fetch all data based on filters.

    Args:
        db: Database session
        location: Optional location name filter
        start_date: Optional start date filter (YYYY-MM-DD)
        end_date: Optional end date filter (YYYY-MM-DD)
        user: Optional user name filter

    Returns:
        List of dictionaries containing weather and location data
    """
    query = db.query(Weather).join(Location)

    # Only get records from the exact user
    if user:
        query = query.filter(Weather.triggered_user.ilike(f"%{user}%"))

    if location:
        query = query.filter(Location.name.ilike(f"%{location}%"))

    if start_date:
        query = query.filter(Weather.date >= start_date)

    if end_date:
        query = query.filter(Weather.date <= end_date)

    if user:
        query = query.filter(Weather.triggered_user.ilike(f"%{user}%"))

    weather_records = query.order_by(Weather.date.desc()).all()

    return [record.to_dict() for record in weather_records]


@router.get("/json")
async def export_json(
    db: Session = Depends(get_db),
    location: Optional[str] = Query(None, description="Filter by location name"),
    start_date: Optional[str] = Query(
        None, description="Start date filter (YYYY-MM-DD)"
    ),
    end_date: Optional[str] = Query(None, description="End date filter (YYYY-MM-DD)"),
):
    """
    Export all data as JSON format.

    Args:
        db: Database session
        location: Optional location name filter
        start_date: Optional start date filter
        end_date: Optional end date filter

    Returns:
        JSON response with weather and location data
    """
    try:
        data = _get_all_data(db, location, start_date, end_date)

        export_metadata = {
            "export_timestamp": datetime.utcnow().isoformat(),
            "export_format": "JSON",
            "record_count": len(data),
            "filters_applied": {
                "location": location,
                "start_date": start_date,
                "end_date": end_date,
            },
        }

        response_data = {"metadata": export_metadata, "data": data}

        return Response(
            content=json.dumps(response_data, indent=2),
            media_type="application/json",
            headers={
                "Content-Disposition": f"attachment; filename=weather_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            },
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Export failed: {str(e)}")


@router.get("/xml")
async def export_xml(
    db: Session = Depends(get_db),
    location: Optional[str] = Query(None, description="Filter by location name"),
    start_date: Optional[str] = Query(
        None, description="Start date filter (YYYY-MM-DD)"
    ),
    end_date: Optional[str] = Query(None, description="End date filter (YYYY-MM-DD)"),
):
    """
    Export all data as XML format.

    Args:
        db: Database session
        location: Optional location name filter
        start_date: Optional start date filter
        end_date: Optional end date filter

    Returns:
        XML response with weather and location data
    """
    try:
        data = _get_all_data(db, location, start_date, end_date)

        # Create XML structure
        root = ET.Element("weather_export")

        # Add metadata
        metadata = ET.SubElement(root, "metadata")
        ET.SubElement(metadata, "export_timestamp").text = datetime.utcnow().isoformat()
        ET.SubElement(metadata, "export_format").text = "XML"
        ET.SubElement(metadata, "record_count").text = str(len(data))

        filters = ET.SubElement(metadata, "filters_applied")
        ET.SubElement(filters, "location").text = location or ""
        ET.SubElement(filters, "start_date").text = start_date or ""
        ET.SubElement(filters, "end_date").text = end_date or ""

        # Add data
        data_element = ET.SubElement(root, "data")

        for record in data:
            record_element = ET.SubElement(data_element, "weather_record")

            for key, value in record.items():
                element = ET.SubElement(record_element, key)
                element.text = str(value) if value is not None else ""

        # Convert to string
        xml_str = ET.tostring(root, encoding="unicode", method="xml")

        return Response(
            content=xml_str,
            media_type="application/xml",
            headers={
                "Content-Disposition": f"attachment; filename=weather_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xml"
            },
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Export failed: {str(e)}")


@router.get("/csv")
async def export_csv(
    db: Session = Depends(get_db),
    location: Optional[str] = Query(None, description="Filter by location name"),
    start_date: Optional[str] = Query(
        None, description="Start date filter (YYYY-MM-DD)"
    ),
    end_date: Optional[str] = Query(None, description="End date filter (YYYY-MM-DD)"),
):
    """
    Export all data as CSV format.

    Args:
        db: Database session
        location: Optional location name filter
        start_date: Optional start date filter
        end_date: Optional end date filter

    Returns:
        CSV response with weather and location data
    """
    try:
        data = _get_all_data(db, location, start_date, end_date)

        if not data:
            return {"error": 404, "detail": "No data found with the specified filters"}

        # Create CSV content
        output = StringIO()

        # Write metadata as comments
        output.write(f"# Weather Data Export\n")
        output.write(f"# Export Timestamp: {datetime.now().isoformat()}\n")
        output.write(f"# Export Format: CSV\n")
        output.write(f"# Record Count: {len(data)}\n")
        output.write(
            f"# Filters Applied - Location: {location or 'None'}, Start Date: {start_date or 'None'}, End Date: {end_date or 'None'}\n"
        )
        output.write(f"#\n")

        # Write CSV data
        fieldnames = data[0].keys()
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

        csv_content = output.getvalue()
        output.close()

        return Response(
            content=csv_content,
            media_type="text/csv",
            headers={
                "Content-Disposition": \
                f"attachment; \
                filename=weather_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            },
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Export failed: {str(e)}")


@router.get("/locations/json")
async def export_locations_json(db: Session = Depends(get_db)):
    """
    Export all locations as JSON format.

    Returns:
        JSON response with location data
    """
    try:
        locations = db.query(Location).order_by(Location.name).all()
        data = [location.to_dict() for location in locations]

        export_metadata = {
            "export_timestamp": datetime.utcnow().isoformat(),
            "export_format": "JSON",
            "record_count": len(data),
            "data_type": "locations_only",
        }

        response_data = {"metadata": export_metadata, "data": data}

        return Response(
            content=json.dumps(response_data, indent=2),
            media_type="application/json",
            headers={
                "Content-Disposition": f"attachment; filename=locations_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            },
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Export failed: {str(e)}")


@router.get("/weather/json")
async def export_weather_json(
    db: Session = Depends(get_db),
    location: Optional[str] = Query(None, description="Filter by location name"),
    start_date: Optional[str] = Query(
        None, description="Start date filter (YYYY-MM-DD)"
    ),
    end_date: Optional[str] = Query(None, description="End date filter (YYYY-MM-DD)"),
):
    """
    Export weather data only as JSON format.

    Returns:
        JSON response with weather data only
    """
    try:
        query = db.query(Weather)

        # Apply filters
        if location:
            query = query.join(Location).filter(Location.name.ilike(f"%{location}%"))

        if start_date:
            query = query.filter(Weather.date >= start_date)

        if end_date:
            query = query.filter(Weather.date <= end_date)

        weather_records = query.order_by(Weather.date.desc()).all()
        data = [record.to_dict() for record in weather_records]

        export_metadata = {
            "export_timestamp": datetime.utcnow().isoformat(),
            "export_format": "JSON",
            "record_count": len(data),
            "data_type": "weather_only",
            "filters_applied": {
                "location": location,
                "start_date": start_date,
                "end_date": end_date,
            },
        }

        response_data = {"metadata": export_metadata, "data": data}

        return Response(
            content=json.dumps(response_data, indent=2),
            media_type="application/json",
            headers={
                "Content-Disposition": \
                f"attachment; \
                filename=weather_only_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            },
        )

    except HTTPException as e:
        return {"error": 500, "detail": f"Database error: {str(e)}"}
