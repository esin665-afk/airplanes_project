"""
Модуль для работы с API nominatim.openstreetmap.org и opensky-network.org.
"""

import requests

from src.abc_classes import BaseAPI


class AeroplanesAPI(BaseAPI):
    """
    Класс для работы с API сервисов nominatim и opensky.
    """

    nominatim_url = "https://nominatim.openstreetmap.org/search"
    opensky_url = "https://opensky-network.org/api/states/all"

    def get_country_coordinates(self, country: str) -> dict:
        """
        Получает географические координаты страны через nominatim.
        """
        params = {
            "q": country,
            "format": "json",
            "limit": 1,
        }
        headers = {
            "User-Agent": "airplanes-project/1.0",
        }
        response = requests.get(
            self.nominatim_url, params=params, headers=headers
        )
        response.raise_for_status()
        data = response.json()

        if not data:
            raise ValueError(f"Страна '{country}' не найдена")

        return data[0]

    def get_aeroplanes(self, country: str) -> list:
        """
        Получает информацию о самолётах в воздушном пространстве страны.
        """
        coordinates = self.get_country_coordinates(country)
        bounding_box = coordinates["boundingbox"]

        # boundingbox: [south, north, west, east]
        params = {
            "lamin": bounding_box[0],
            "lamax": bounding_box[1],
            "lomin": bounding_box[2],
            "lomax": bounding_box[3],
        }

        response = requests.get(self.opensky_url, params=params)
        response.raise_for_status()
        data = response.json()

        if not data or "states" not in data:
            return []

        return data["states"]
