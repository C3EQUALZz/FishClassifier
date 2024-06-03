from typing import Any

import json
import logging
import pathlib

logger = logging.getLogger(__name__)


class Settings:
    """
    Класс для работы с настройками приложения, хранящимися в JSON-файле.
    """
    _instance = None

    json_file: str = "settings.json"
    app_path: pathlib.Path = pathlib.Path.cwd()
    settings_path: pathlib.Path = app_path / json_file

    if not settings_path.is_file():
        logger.warning(f"\"settings.json\" not found! check in the folder {settings_path}")

    def __new__(cls, *args, **kwargs) -> "Settings":
        """
        Singleton, так как к настройкам я могу обратиться в любом View,
        соответственно для оптимизации выбран данный паттерн.
        """
        if not cls._instance:
            cls._instance = super(Settings, cls).__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """
        Инициализирует объект Settings, загружая настройки из JSON-файла.
        """
        self._items: dict[str, Any] = {}
        self.__deserialize()

    @property
    def items(self) -> dict[str, Any]:
        """
        Свойство - геттер, которое возвращает словарь со всеми параметрами
        :return: словарь с параметрами приложения
        """
        return self._items

    @items.setter
    def items(self, value: dict[str, Any]) -> None:
        """
        Свойство - cеттер, которое устанавливает словарь со всеми параметрами в Runtime и обновляет файл.
        :param value: Словарь, с параметрами, которые хотим поставить.
        :return: Ничего не возвращает
        """
        self._items = value
        self.__serialize()

    def __getitem__(self, key: str) -> Any:
        """
        Возвращает значение настройки по ключу.

        Parameters:
        key (str): Ключ настройки.

        Returns:
        Any: Значение настройки.
        """
        return self._items.get(key)

    def __serialize(self) -> None:
        """
        Сериализует текущие настройки в JSON-файл.
        """
        with open(self.settings_path, "w", encoding='utf-8') as write:
            json.dump(self._items, write, indent=4)

    def __deserialize(self) -> None:
        """
        Десериализует настройки из JSON-файла.
        """
        with open(self.settings_path, "r", encoding='utf-8') as reader:
            self._items = json.loads(reader.read())
