"""
# utils.py
# Sharing constants and functions across the application
"""
import tomllib

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
        level (int): The level of the message (0: info, 1: warn, 2: error).
    """
    config = tomllib.load(open("settings.toml", "rb"))
    level_map = {
        "info": 0,
        "warn": 1,
        "error": 2
    }

    log_level = level_map.get(level, 0)
    if log_level > config.get("app", {}).get("log_level", 0):
        return
    print(f"{COLOR[level]}[{level.upper()}]{COLOR['reset']} {message}")
