# read version from installed package
from importlib.metadata import version
__version__ = version("weather_yl6088")
from .weather_yl6088 import (
    celsius_to_fahrenheit,
    summarize_temperatures,
    clean_readings,
)