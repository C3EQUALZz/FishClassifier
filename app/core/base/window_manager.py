from collections import deque
from typing import Deque, Optional, Type

import app.core.base.factory as factories_namespace
import app.core.interfaces as interfaces_namespace


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
            raise Exception('View factory or controller factory must be set')

        # Получение View и Controller через фабрики
        view = self._view_factory.create_view(window_type)
        controller = self._controller_factory.create_controller(view)

        # Закрытие текущего окна, если оно есть
        if self._window_history:
            self._window_history[-1].hide_window()

        # Добавление нового окна в историю и его открытие
        self._window_history.append(view)
        view.show_window()
        # controller.initialize()

    def go_back(self):
        # Возврат к предыдущему окну в истории
        if len(self._window_history) > 1:
            current_window = self._window_history.pop()
            current_window.close_window()
            self._window_history[-1].show_window()

    def get_current_window(self):
        return self._window_history[-1]
