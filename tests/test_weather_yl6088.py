"""Tests for the weather_yl6088 package."""

import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from weather_yl6088 import (
    celsius_to_fahrenheit,
    clean_readings,
    summarize_temperatures,
)


@pytest.mark.parametrize(
    "celsius, expected",
    [(0, 32), (100, 212), (-40, -40), (37, 98.6), (-273.15, -459.67)],
)
def test_celsius_to_fahrenheit(celsius, expected):
    """Check conversion for five known temperatures."""
    assert celsius_to_fahrenheit(celsius) == pytest.approx(expected)


@pytest.mark.parametrize(
    "bad_input, expected_error",
    [
        (-274, ValueError),
        ("20", TypeError),
        (None, TypeError),
        (True, TypeError),
    ],
)
def test_celsius_to_fahrenheit_invalid(bad_input, expected_error):
    """Reject invalid temperatures and input types."""
    with pytest.raises(expected_error):
        celsius_to_fahrenheit(bad_input)


def test_summarize_temperatures():
    """Check summary statistics while ignoring NaN."""
    result = summarize_temperatures([10.0, float("nan"), 20.0])

    assert result["mean"] == pytest.approx(15.0)
    assert result["min"] == 10.0
    assert result["max"] == 20.0
    assert result["n_missing"] == 1


@pytest.mark.parametrize("temps", [[], [float("nan"), float("nan")]])
def test_summarize_temperatures_no_valid_readings(temps):
    """Reject inputs without valid readings."""
    with pytest.raises(ValueError, match="no valid temperature readings"):
        summarize_temperatures(temps)


@pytest.fixture
def raw_readings():
    """Return unsorted readings with missing and erroneous temperatures."""
    return pd.DataFrame({
        "station": ["JFK", "CPK", "JFK", "CPK", "LGA"],
        "date": [
            "2026-07-02",
            "2026-07-01",
            "2026-07-01",
            "2026-07-02",
            "2026-07-01",
        ],
        "temp_c": [30.0, 25.0, float("nan"), 999.0, 28.0],
    })


def test_raw_readings_fixture(raw_readings):
    """Check fixture structure and missing values."""
    assert list(raw_readings.columns) == ["station", "date", "temp_c"]
    assert len(raw_readings) == 5
    assert raw_readings.isna().sum().to_dict() == {
        "station": 0,
        "date": 0,
        "temp_c": 1,
    }


def test_clean_readings(raw_readings):
    """Check cleaned values, sorting, columns, index, and dtypes."""
    expected = pd.DataFrame({
        "station": ["CPK", "JFK", "LGA"],
        "date": ["2026-07-01", "2026-07-02", "2026-07-01"],
        "temp_c": [25.0, 30.0, 28.0],
        "temp_f": [77.0, 86.0, 82.4],
    })

    result = clean_readings(raw_readings)

    assert_frame_equal(result, expected)
