"""
Тесты для функций фильтрации.
"""

from main import (
    filter_aeroplanes_by_altitude,
    filter_aeroplanes_by_country,
    get_top_aeroplanes,
)


def test_get_top_aeroplanes(sample_aeroplanes):
    """Тест: топ N самолётов по высоте."""
    top_2 = get_top_aeroplanes(sample_aeroplanes, 2)
    assert len(top_2) == 2
    assert top_2[0].baro_altitude >= top_2[1].baro_altitude


def test_get_top_aeroplanes_empty():
    """Тест: пустой список возвращает пустой список."""
    assert get_top_aeroplanes([], 5) == []


def test_filter_aeroplanes_by_country(sample_aeroplanes):
    """Тест: фильтрация по стране регистрации."""
    result = filter_aeroplanes_by_country(sample_aeroplanes, ["Russia"])
    assert len(result) == 2


def test_filter_aeroplanes_by_country_empty(sample_aeroplanes):
    """Тест: пустой список стран возвращает всех."""
    result = filter_aeroplanes_by_country(sample_aeroplanes, [])
    assert len(result) == 4


def test_filter_aeroplanes_by_altitude(sample_aeroplanes):
    """Тест: фильтрация по диапазону высот."""
    result = filter_aeroplanes_by_altitude(
        sample_aeroplanes, "10000 - 11500"
    )
    assert len(result) == 2  # 11000 и 10203.18


def test_filter_aeroplanes_by_altitude_invalid(sample_aeroplanes):
    """Тест: некорректный диапазон возвращает всех."""
    result = filter_aeroplanes_by_altitude(sample_aeroplanes, "invalid")
    assert len(result) == 4
