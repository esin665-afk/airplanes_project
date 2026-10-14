"""
Тесты для класса JSONSaver.
"""


def test_add_aeroplane(temp_json_saver, sample_aeroplane):
    """Тест: добавление самолёта в файл."""
    temp_json_saver.add_aeroplane(sample_aeroplane)
    data = temp_json_saver.get_aeroplanes({})
    assert len(data) == 1
    assert data[0]["callsign"] == "UAL1621"


def test_get_aeroplanes_by_criteria(temp_json_saver, sample_aeroplanes):
    """Тест: получение самолётов по критериям."""
    for aeroplane in sample_aeroplanes:
        temp_json_saver.add_aeroplane(aeroplane)

    result = temp_json_saver.get_aeroplanes(
        {"origin_country": "Russia"}
    )
    assert len(result) == 2


def test_delete_aeroplane(temp_json_saver, sample_aeroplane):
    """Тест: удаление самолёта."""
    temp_json_saver.add_aeroplane(sample_aeroplane)
    assert len(temp_json_saver.get_aeroplanes({})) == 1

    temp_json_saver.delete_aeroplane(sample_aeroplane)
    assert len(temp_json_saver.get_aeroplanes({})) == 0


def test_get_empty_file(temp_json_saver):
    """Тест: пустой файл возвращает пустой список."""
    result = temp_json_saver.get_aeroplanes({})
    assert result == []


def test_add_multiple_aeroplanes(temp_json_saver, sample_aeroplanes):
    """Тест: добавление нескольких самолётов."""
    for aeroplane in sample_aeroplanes:
        temp_json_saver.add_aeroplane(aeroplane)

    result = temp_json_saver.get_aeroplanes({})
    assert len(result) == 4
