"""
Модуль с абстрактными классами для работы с API и файлами.
"""

from abc import ABC, abstractmethod


class BaseAPI(ABC):
    """
    Абстрактный класс для работы с API внешних сервисов.
    """

    @abstractmethod
    def get_country_coordinates(self, country: str) -> dict:
        """
        Получает географические координаты страны.
        """
        pass

    @abstractmethod
    def get_aeroplanes(self, country: str) -> list:
        """
        Получает информацию о самолётах в воздушном пространстве страны.
        """
        pass


class BaseFileSaver(ABC):
    """
    Абстрактный класс для работы с файлами.
    """

    @abstractmethod
    def add_aeroplane(self, aeroplane: dict) -> None:
        """
        Добавляет информацию о самолёте в файл.
        """
        pass

    @abstractmethod
    def get_aeroplanes(self, criteria: dict) -> list:
        """
        Получает данные из файла по указанным критериям.
        """
        pass

    @abstractmethod
    def delete_aeroplane(self, aeroplane: dict) -> None:
        """
        Удаляет информацию о самолёте из файла.
        """
        pass
