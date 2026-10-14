"""
Модуль с классом Aeroplane (Самолёт).
"""

from typing import Any, List, Optional


class Aeroplane:
    """
    Класс для представления самолёта.
    """

    def __init__(
        self,
        callsign: str,
        origin_country: str,
        velocity: float,
        baro_altitude: float,
        icao24: str = "",
        longitude: Optional[float] = None,
        latitude: Optional[float] = None,
        on_ground: bool = False,
    ) -> None:
        """
        Инициализация самолёта с валидацией данных.
        """
        if not callsign or not isinstance(callsign, str):
            raise ValueError("Позывной должен быть непустой строкой")
        if not origin_country or not isinstance(origin_country, str):
            raise ValueError("Страна регистрации должна быть непустой строкой")
        if velocity is None or velocity < 0:
            raise ValueError("Скорость должна быть неотрицательной")
        if baro_altitude is None or baro_altitude < 0:
            raise ValueError("Высота должна быть неотрицательной")

        self.callsign = callsign.strip()
        self.origin_country = origin_country.strip()
        self.velocity = velocity
        self.baro_altitude = baro_altitude
        self.icao24 = icao24
        self.longitude = longitude
        self.latitude = latitude
        self.on_ground = on_ground

    def __repr__(self) -> str:
        """Строковое представление самолёта."""
        return (
            f"Aeroplane('{self.callsign}', '{self.origin_country}', "
            f"{self.velocity}, {self.baro_altitude})"
        )

    def __str__(self) -> str:
        """Человекочитаемое представление."""
        return (
            f"Самолёт {self.callsign} ({self.origin_country}): "
            f"скорость {self.velocity} м/с, высота {self.baro_altitude} м"
        )

    def __eq__(self, other: "Aeroplane") -> bool:
        """Сравнение по скорости и высоте."""
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return (
            self.velocity == other.velocity
            and self.baro_altitude == other.baro_altitude
        )

    def __lt__(self, other: "Aeroplane") -> bool:
        """Сравнение по высоте (меньше)."""
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return self.baro_altitude < other.baro_altitude

    def __gt__(self, other: "Aeroplane") -> bool:
        """Сравнение по высоте (больше)."""
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return self.baro_altitude > other.baro_altitude

    @classmethod
    def cast_to_object_list(cls, aeroplanes_data: List[List[Any]]) -> List["Aeroplane"]:
        """
        Преобразует список данных от API в список объектов Aeroplane.
        """
        result = []
        for item in aeroplanes_data:
            try:
                if len(item) < 10:
                    continue

                icao24 = item[0] or ""
                callsign = (item[1] or "").strip()
                origin_country = item[2] or ""
                longitude = item[5]
                latitude = item[6]
                baro_altitude = item[7]
                on_ground = item[8] if len(item) > 8 else False
                velocity = item[9] if len(item) > 9 else None

                # Пропускаем самолёты без ключевых данных
                if not callsign or not origin_country:
                    continue
                if velocity is None or baro_altitude is None:
                    continue

                aeroplane = cls(
                    callsign=callsign,
                    origin_country=origin_country,
                    velocity=float(velocity),
                    baro_altitude=float(baro_altitude),
                    icao24=icao24,
                    longitude=longitude,
                    latitude=latitude,
                    on_ground=on_ground,
                )
                result.append(aeroplane)
            except (ValueError, TypeError, IndexError):
                # Пропускаем некорректные данные
                continue
        return result
