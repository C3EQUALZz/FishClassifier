
from PySide6.QtCore import QPropertyAnimation

import abc
import app.core.interfaces as interfaces_namespace
import app.views.login.helpers as helpers_namespace


class ProgressDecorator(abc.ABC):
    """
    Абстрактный класс для декораторов.
    У нас могут быть разные зарузки, поэтому выбран был паттерн декоратор для добавления возможностей.
    """
    def __init__(self,
                 progress: interfaces_namespace.Progress,
                 ui_login: helpers_namespace.UiLogin
                 ) -> None:

        self.progress = progress
        self.ui = ui_login
        self.property_animation = QPropertyAnimation(self.ui.frame_widgets, b"geometry")

    @abc.abstractmethod
    def start(self) -> None:
        """
        Абстрактный метод настройки индикатора выполнения.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def animation(self) -> None:
        """
        Абстрактный метод для обработки анимации индикатора выполнения.
        """
        raise NotImplementedError

    def show(self) -> None:
        """
        Показывает индикатор выполнения и запускает анимацию.
        """
        self.animation()
        self.progress.show()
