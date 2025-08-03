"""
# model/db.py
# This module sets up the database connection and base class for SQLAlchemy models.
"""
import os
import tomllib
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

config_path = os.path.join(os.path.dirname(__file__), '..', 'settings.toml')
with open(config_path, "rb") as config_file:
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file {config_path} not found.")
    config = tomllib.load(config_file)
DATABASE_URL = config.get("database", {}).get("url", None)
pool_size = config.get("database", {}).get("pool_size", 2)

if not DATABASE_URL:
    raise ValueError("Please set up a database URL in settings.toml under [database] section first")

engine = create_engine(DATABASE_URL, pool_size=pool_size, max_overflow=0)
Base = declarative_base()
