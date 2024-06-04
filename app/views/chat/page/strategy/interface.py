from abc import ABC, abstractmethod
from PySide6.QtWidgets import QWidget


class MessageStrategy(ABC):
    """Абстрактный класс стратегии отправки сообщений."""

    @abstractmethod
    def send_message(self, message: str, parent: QWidget) -> None:
        ...
