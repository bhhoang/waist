"""
# model/db.py
# This module sets up the database connection and base class for SQLAlchemy models.
"""

import tomllib
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker
from utils import fprint

config_path = os.path.join(os.path.dirname(__file__), "..", "settings.toml")
with open(config_path, "rb") as config_file:
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file {config_path} not found.")
    config = tomllib.load(config_file)

DB_URL = config.get("database", {}).get("url", None)
DATABASE_URL = os.getenv("DATABASE_URL", DB_URL)
pool = config.get("database", {}).get("pool_size", 10)
pool_size = int(os.getenv("DATABASE_POOL_SIZE", pool))

if not DATABASE_URL:
    raise ValueError(
        "Please set up a database URL in settings.toml under [database] section first"
    )

engine = create_engine(
    DATABASE_URL, 
    pool_size=pool_size, 
    max_overflow=20,  # Allow 20 overflow connections
    pool_timeout=30,  # Wait 30 seconds for a connection
    pool_recycle=3600,  # Recycle connections every hour
    pool_pre_ping=True  # Verify connections before use
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """
    Dependency to get a database session.
    Yields a database session for use in requests.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def _import_models() -> None:
    """
    Import all models to ensure they are registered with SQLAlchemy.
    This is necessary for the Base.metadata.create_all() to work correctly.
    """
    try:
        from . import location, weather
    except ImportError as e:
        fprint(f"Error importing models: {e}", level="error")
        raise e

def _check_tables() -> bool:
    """
    Check if all the tables exist in the database.
    Returns True if tables exist, False otherwise.
    """
    try:
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name
            """))
            created_tables = [row[0] for row in result]
            return bool(created_tables)
    except Exception as e:
        fprint(f"Error checking tables: {e}", level="error")
        return False

def create_tables() -> None:
    """Create all database tables"""
    try:
        if _check_tables():
            fprint("Tables already exist in the database.", level="info")
            return
        _import_models()
        table_names = list(Base.metadata.tables.keys())
        if table_names:
            fprint(f"Creating tables: {', '.join(table_names)}", level="info")
        else:
            fprint("Warning: No tables found in metadata", level="warn")
        Base.metadata.create_all(bind=engine)

    except Exception as e:
        fprint(f"Error creating database tables: {e}", level="error")
        raise e


def drop_tables() -> None:
    """Drop all database tables"""
    Base.metadata.drop_all(bind=engine)
    fprint("Database tables dropped successfully!", level="info")


def check_connection() -> bool:
    """Check if the database connection is working"""
    try:
        with engine.connect() as connection:
            connection.execute("SELECT 1")
            fprint("Database connection is working.", level="info")
            return True
    except Exception as e:
        fprint(f"Database connection failed: {e}", level="error")
        return False
    return True
