import abc

import app.core.base as base


class AbstractController(abc.ABC):
    """
    Абстрактный класс контроллер, который должен реализовывать каждый контроллер
    """
    def __init__(self, view) -> None:
        self.view = view
        self.window_manager = base.WindowManager()
