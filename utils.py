"""
# utils.py
# Sharing constants and functions across the application
"""
import tomllib
import os
import random

ALPHABET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

COLOR = {
    "error": "\033[91m",  # Red
    "warn": "\033[93m",  # Yellow
    "info": "\033[92m",  # Green
    "reset": "\033[0m",  # Reset color
}


def fprint(message: str, level: str = "info") -> None:
    """
    Formatted print function to display messages with a specific level.

    Args:
        message (str): The message to print.
        level (int): The level of the message (0: error, 1: warn, 2: info).
    """

    config = tomllib.load(open("settings.toml", "rb"))
    threshold = config.get("app", {}).get("log_level", 0)
    level_map = {
        "error": 0,
        "warn": 1,
        "info": 2
    }

    log_level = level_map.get(level, 0)
    if log_level > threshold:
        return
    print(f"{COLOR[level]}[{level.upper()}]{COLOR['reset']} {message}")


def random_user_string(length: int = 8) -> str:
    """
    Generate a random user string of specified length.

    Args:
        length (int): Length of the random string to generate.

    Returns:
        str: Randomly generated string.
    """
    return ''.join(random.choice(ALPHABET) for _ in range(length))

def convert_weather_code(code: int) -> str:
    """
    Convert weather code to human-readable format.
    """
    weather_code_map = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Drizzle: Light intensity",
        53: "Drizzle: Moderate intensity",
        55: "Drizzle: Dense intensity",
        56: "Freezing Drizzle: Light intensity",
        57: "Freezing Drizzle: Dense intensity",
        61: "Rain: Slight intensity",
        63: "Rain: Moderate intensity",
        65: "Rain: Heavy intensity",
        66: "Freezing Rain: Light intensity",
        67: "Freezing Rain: Heavy intensity",
        71: "Snow fall: Slight intensity",
        73: "Snow fall: Moderate intensity",
        75: "Snow fall: Heavy intensity",
        77: "Snow grains",
        80: "Rain showers: Slight",
        81: "Rain showers: Moderate",
        82: "Rain showers: Violent",
        85: "Snow showers: Slight",
        86: "Snow showers: Heavy",
        95: "Thunderstorm: Slight or moderate",
        96: "Thunderstorm with slight hail",
        99: "Thunderstorm with heavy hail",
    }

    return weather_code_map.get(code, "Unknown weather code")

def reverse_weather_code(description: str) -> int:
    """
    Convert human-readable weather description to code.
    """
    weather_code_map = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Drizzle: Light intensity",
        53: "Drizzle: Moderate intensity",
        55: "Drizzle: Dense intensity",
        56: "Freezing Drizzle: Light intensity",
        57: "Freezing Drizzle: Dense intensity",
        61: "Rain: Slight intensity",
        63: "Rain: Moderate intensity",
        65: "Rain: Heavy intensity",
        66: "Freezing Rain: Light intensity",
        67: "Freezing Rain: Heavy intensity",
        71: "Snow fall: Slight intensity",
        73: "Snow fall: Moderate intensity",
        75: "Snow fall: Heavy intensity",
        77: "Snow grains",
        80: "Rain showers: Slight",
        81: "Rain showers: Moderate",
        82: "Rain showers: Violent",
        85: "Snow showers: Slight",
        86: "Snow showers: Heavy",
        95: "Thunderstorm: Slight or moderate",
        96: "Thunderstorm with slight hail",
        99: "Thunderstorm with heavy hail",
    }

    reverse_map = {v: k for k, v in weather_code_map.items()}
    return reverse_map.get(description, -1)
