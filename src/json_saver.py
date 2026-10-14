"""
Модуль для сохранения информации о самолётах в JSON-файл.
"""

import json
import os
from typing import Any, Dict, List

from src.abc_classes import BaseFileSaver


class JSONSaver(BaseFileSaver):
    """
    Класс для сохранения информации о самолётах в JSON-файл.
    """

    def __init__(self, filename: str = "aeroplanes.json") -> None:
        """
        Инициализация JSONSaver.
        """
        self.filename = filename
        # Создаём пустой файл, если его нет
        if not os.path.exists(self.filename):
            with open(self.filename, "w", encoding="utf-8") as file:
                json.dump([], file, ensure_ascii=False, indent=2)

    def _read_file(self) -> List[Dict[str, Any]]:
        """
        Читает данные из JSON-файла.
        """
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _write_file(self, data: List[Dict[str, Any]]) -> None:
        """
        Записывает данные в JSON-файл.
        """
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)

    @staticmethod
    def _aeroplane_to_dict(aeroplane: Any) -> Dict[str, Any]:
        """
        Преобразует объект Aeroplane в словарь.
        """
        if isinstance(aeroplane, dict):
            return aeroplane
        return {
            "callsign": aeroplane.callsign,
            "origin_country": aeroplane.origin_country,
            "velocity": aeroplane.velocity,
            "baro_altitude": aeroplane.baro_altitude,
            "icao24": aeroplane.icao24,
            "longitude": aeroplane.longitude,
            "latitude": aeroplane.latitude,
            "on_ground": aeroplane.on_ground,
        }

    def add_aeroplane(self, aeroplane: Any) -> None:
        """
        Добавляет самолёт в JSON-файл.
        """
        data = self._read_file()
        data.append(self._aeroplane_to_dict(aeroplane))
        self._write_file(data)

    def get_aeroplanes(self, criteria: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Получает самолёты из файла по критериям.
        """
        data = self._read_file()
        result = []

        for aeroplane in data:
            match = True
            for key, value in criteria.items():
                if aeroplane.get(key) != value:
                    match = False
                    break
            if match:
                result.append(aeroplane)

        return result

    def delete_aeroplane(self, aeroplane: Any) -> None:
        """
        Удаляет самолёт из JSON-файла.
        """
        data = self._read_file()
        target = self._aeroplane_to_dict(aeroplane)

        # Удаляем первое совпадение по icao24 или callsign
        for i, item in enumerate(data):
            if (
                item.get("icao24") == target.get("icao24")
                and item.get("callsign") == target.get("callsign")
            ):
                data.pop(i)
                break

        self._write_file(data)
