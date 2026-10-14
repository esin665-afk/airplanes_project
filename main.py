"""
Основной модуль для взаимодействия с пользователем.
Запустите: python main.py
"""

from src.aeroplane import Aeroplane
from src.api import AeroplanesAPI
from src.json_saver import JSONSaver


def get_top_aeroplanes(
    aeroplanes: list, top_n: int
) -> list:
    """
    Возвращает топ N самолётов по высоте полёта.
    """
    if not aeroplanes:
        return []
    sorted_aeroplanes = sorted(
        aeroplanes, key=lambda a: a.baro_altitude, reverse=True
    )
    return sorted_aeroplanes[:top_n]


def filter_aeroplanes_by_country(
    aeroplanes: list, countries: list
) -> list:
    """
    Фильтрует самолёты по стране регистрации.
    """
    if not countries:
        return aeroplanes
    countries_lower = [c.lower().strip() for c in countries]
    return [
        a for a in aeroplanes
        if a.origin_country.lower() in countries_lower
    ]


def filter_aeroplanes_by_altitude(
    aeroplanes: list, altitude_range: str
) -> list:
    """
    Фильтрует самолёты по диапазону высоты полёта.
    """
    if not altitude_range or "-" not in altitude_range:
        return aeroplanes
    try:
        parts = altitude_range.split("-")
        min_alt = float(parts[0].strip())
        max_alt = float(parts[1].strip())
    except (ValueError, IndexError):
        return aeroplanes

    return [
        a for a in aeroplanes
        if min_alt <= a.baro_altitude <= max_alt
    ]


def print_aeroplanes(aeroplanes: list) -> None:
    """
    Выводит информацию о самолётах в консоль.
    """
    if not aeroplanes:
        print("Самолёты не найдены.")
        return
    for i, aeroplane in enumerate(aeroplanes, start=1):
        print(f"{i}. {aeroplane}")


def user_interaction() -> None:
    """
    Функция для взаимодействия с пользователем через консоль.
    """
    api = AeroplanesAPI()
    saver = JSONSaver("aeroplanes.json")

    country = input("Введите название страны: ").strip()
    if not country:
        print("Название страны не может быть пустым.")
        return

    try:
        raw_data = api.get_aeroplanes(country)
    except Exception as e:
        print(f"Ошибка при получении данных: {e}")
        return

    aeroplanes = Aeroplane.cast_to_object_list(raw_data)
    if not aeroplanes:
        print("Самолёты не найдены.")
        return

    print(f"Найдено самолётов: {len(aeroplanes)}")

    # Сохраняем в файл
    for aeroplane in aeroplanes:
        saver.add_aeroplane(aeroplane)
    print("Данные сохранены в файл aeroplanes.json")

    # Топ N по высоте
    try:
        top_n = int(input("Введите количество самолётов для вывода в топ N: "))
    except ValueError:
        print("Некорректное число. Показываем все.")
        top_n = len(aeroplanes)

    top_aeroplanes = get_top_aeroplanes(aeroplanes, top_n)
    print(f"\nТоп {top_n} самолётов по высоте полёта:")
    print_aeroplanes(top_aeroplanes)

    # Фильтр по стране регистрации
    filter_words = input(
        "\nВведите названия стран для фильтрации "
        "(через пробел, Enter для пропуска): "
    ).split()

    if filter_words:
        filtered = filter_aeroplanes_by_country(aeroplanes, filter_words)
        print(f"\nСамолёты стран {filter_words}:")
        print_aeroplanes(filtered)

    # Фильтр по диапазону высот
    altitude_range = input(
        "\nВведите диапазон высот (например, 10000 - 15000, "
        "Enter для пропуска): "
    ).strip()

    if altitude_range:
        ranged = filter_aeroplanes_by_altitude(aeroplanes, altitude_range)
        print(f"\nСамолёты с высотой {altitude_range}:")
        print_aeroplanes(ranged)


if __name__ == "__main__":
    user_interaction()
