from collections import deque
from typing import Deque, Optional, Type

import app.core.base.factory as factories_namespace
import app.core.interfaces as interfaces_namespace
import logging

logger = logging.getLogger(__name__)


class WindowManager:
    _instance: Optional['WindowManager'] = None
    _view_factory: Optional[factories_namespace.ViewFactory]
    _controller_factory: Optional[Type[factories_namespace.ControllerFactory]]
    _window_history: Deque[interfaces_namespace.ViewStrategy]

    def __new__(cls,
                view_factory: Optional[factories_namespace.ViewFactory] = None,
                controller_factory: Optional[factories_namespace.ControllerFactory] = None
                ) -> "WindowManager":

        if cls._instance is None:
            cls._instance = super(WindowManager, cls).__new__(cls)
            cls._instance._view_factory = view_factory
            cls._instance._controller_factory = controller_factory
            cls._instance._window_history = deque(maxlen=5)
        return cls._instance

    def switch_to_window(self, window_type: str) -> None:

        if self._view_factory is None or self._controller_factory is None:
            logger.exception('Необходимо установить ViewFactory или ControllerFactory')
            raise Exception('Необходимо установить ViewFactory или ControllerFactory')

        self.view = self._view_factory.create_view(window_type)
        logger.debug(f"Показываем новое окно: {self.view}")

        self.controller = self._controller_factory.create_controller(self.view)

        logger.debug(f"Создан view: {self.view}, controller: {self.controller}")

        if self._window_history:
            current_view = self._window_history[-1]
            logger.debug(f"Прячу текущее окно: {current_view}")
            current_view.hide_window()

        self._window_history.append(self.view)
        self.view.show_window()
        self.controller.initialize()

    def go_back(self):
        # Возврат к предыдущему окну в истории
        if len(self._window_history) > 1:
            current_window = self._window_history.pop()
            logger.debug(f"Закрываю текущее окно: {current_window}")
            current_window.close_window()

            previous_window = self._window_history[-1]
            logger.debug(f"Показываю прошлое окно: {previous_window}")
            previous_window.show_window()

    def get_current_window(self):

        if self._window_history:
            current_window = self._window_history[-1]
            logger.debug(f"Текущее окно: {current_window}")
            return current_window

        logger.debug("Нет текущего окна")
        return None
