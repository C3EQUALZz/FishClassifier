import app.controllers.login as login_namespace
import app.controllers.main as main_namespace
import app.views as views_namespace
import app.core.abstract as base_namespace
import app.core.interfaces as interfaces_namespace
import logging

logger = logging.getLogger(__name__)


class ControllerFactory:
    """
    Класс предназначен для создания контроллеров,
    соответствующих определенным представлениям. Это реализация шаблона
    проектирования "Фабрика" (Factory), который обеспечивает удобный способ
    создания объектов с определенным интерфейсом.
    """

    @staticmethod
    def create_controller(view: interfaces_namespace.ViewStrategy) -> base_namespace.AbstractController | None:
        """
        Создает и возвращает контроллер, соответствующий данному представлению.

        :param view: Представление, для которого требуется создать контроллер.
        :returns: Контроллер, соответствующий данному представлению.
        """
        if isinstance(view, views_namespace.MainView):
            logger.debug("В ControllerFactory.create_controller выбран MainController")
            return main_namespace.MainController(view)
        if isinstance(view, views_namespace.LoginView):
            logger.debug("В ControllerFactory.create_controller выбран LoginController")
            return login_namespace.LoginController(view)

        logger.exception(f"Неизвестное представление: {type(view)}")
        raise ValueError(f"Неизвестное представление: {type(view)}")
