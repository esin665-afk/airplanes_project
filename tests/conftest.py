"""
Фикстуры для тестов проекта airplanes.
"""

import os
import tempfile

import pytest

from src.aeroplane import Aeroplane
from src.json_saver import JSONSaver


@pytest.fixture
def sample_aeroplane():
    """Фикстура: один тестовый самолёт."""
    return Aeroplane(
        callsign="UAL1621",
        origin_country="United States",
        velocity=268.79,
        baro_altitude=10203.18,
        icao24="abc123",
    )


@pytest.fixture
def sample_aeroplanes():
    """Фикстура: список тестовых самолётов."""
    return [
        Aeroplane("A1", "Russia", 250.0, 11000.0, icao24="r1"),
        Aeroplane("A2", "United States", 268.79, 10203.18, icao24="u1"),
        Aeroplane("A3", "Germany", 200.0, 9000.0, icao24="g1"),
        Aeroplane("A4", "Russia", 300.0, 12000.0, icao24="r2"),
    ]


@pytest.fixture
def temp_json_saver():
    """Фикстура: JSONSaver с временным файлом."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False
    ) as f:
        filepath = f.name

    saver = JSONSaver(filepath)
    yield saver

    # Чистим
    if os.path.exists(filepath):
        os.remove(filepath)
