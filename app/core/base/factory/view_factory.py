import app.views.chat as chat_view
import app.views.login as login_view
import app.core.interfaces as interfaces


class ViewFactory:
    """
    Класс ViewFactory предназначен для создания представлений,
    соответствующих определенным типам представлений. Это реализация шаблона
    проектирования "Фабрика" (Factory), который обеспечивает удобный способ
    создания объектов с определенным интерфейсом.
    """
    @staticmethod
    def create_view(view_type: str) -> interfaces.ViewStrategy:
        """
        Создает и возвращает представление, соответствующее данному типу представления.

        :param view_type: Тип представления, для которого требуется создать представление.
        :returns: Представление, соответствующее данному типу представления.
        :exception: Если переданный тип представления не поддерживается, возбуждается исключение.
        """

        if view_type == 'MainWindowView':
            return chat_view.MainView()
        elif view_type == 'LoginWindowView':
            return login_view.LoginView()

        raise Exception("View type not supported")
