"""
Тесты для класса Aeroplane.
"""

import pytest

from src.aeroplane import Aeroplane


def test_aeroplane_initialization(sample_aeroplane):
    """Тест инициализации самолёта."""
    assert sample_aeroplane.callsign == "UAL1621"
    assert sample_aeroplane.origin_country == "United States"
    assert sample_aeroplane.velocity == 268.79
    assert sample_aeroplane.baro_altitude == 10203.18


def test_aeroplane_invalid_callsign():
    """Тест: пустой позывной вызывает ValueError."""
    with pytest.raises(ValueError):
        Aeroplane("", "Russia", 250.0, 10000.0)


def test_aeroplane_invalid_country():
    """Тест: пустая страна вызывает ValueError."""
    with pytest.raises(ValueError):
        Aeroplane("A1", "", 250.0, 10000.0)


def test_aeroplane_negative_velocity():
    """Тест: отрицательная скорость вызывает ValueError."""
    with pytest.raises(ValueError):
        Aeroplane("A1", "Russia", -100.0, 10000.0)


def test_aeroplane_negative_altitude():
    """Тест: отрицательная высота вызывает ValueError."""
    with pytest.raises(ValueError):
        Aeroplane("A1", "Russia", 250.0, -100.0)


def test_aeroplane_comparison_lt():
    """Тест: сравнение по высоте (меньше)."""
    a = Aeroplane("A1", "Russia", 250.0, 9000.0)
    b = Aeroplane("A2", "USA", 260.0, 10000.0)
    assert a < b
    assert not (b < a)


def test_aeroplane_comparison_gt():
    """Тест: сравнение по высоте (больше)."""
    a = Aeroplane("A1", "Russia", 250.0, 9000.0)
    b = Aeroplane("A2", "USA", 260.0, 10000.0)
    assert b > a
    assert not (a > b)


def test_aeroplane_comparison_eq():
    """Тест: равенство по скорости и высоте."""
    a = Aeroplane("A1", "Russia", 250.0, 9000.0)
    b = Aeroplane("A2", "USA", 250.0, 9000.0)
    c = Aeroplane("A3", "Germany", 300.0, 9000.0)
    assert a == b
    assert a != c


def test_cast_to_object_list():
    """Тест: преобразование сырых данных в список объектов."""
    raw_data = [
        ["abc123", "A1  ", "Russia", 0, 0, 10.0, 20.0, 10000.0, False, 250.0],
        ["def456", "A2  ", "USA", 0, 0, 11.0, 21.0, 11000.0, False, 260.0],
    ]
    result = Aeroplane.cast_to_object_list(raw_data)
    assert len(result) == 2
    assert result[0].callsign == "A1"
    assert result[1].callsign == "A2"
    assert result[0].velocity == 250.0


def test_cast_to_object_list_with_invalid_data():
    """Тест: некорректные данные пропускаются."""
    raw_data = [
        ["abc123", "A1", "Russia", 0, 0, 10.0, 20.0, 10000.0, False, 250.0],
        ["def456", "", "USA", 0, 0, 11.0, 21.0, 11000.0, False, 260.0],
        ["ghi789", "A3", "", 0, 0, 12.0, 22.0, 12000.0, False, 270.0],
    ]
    result = Aeroplane.cast_to_object_list(raw_data)
    assert len(result) == 1
    assert result[0].callsign == "A1"
