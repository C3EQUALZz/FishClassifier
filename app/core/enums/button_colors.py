from PySide6.QtGui import QColor
import app.modules.app_settings.settings as settings_namespace
import enum

settings = settings_namespace.Settings()


class ButtonStateColor(enum.Enum):
    """
    Перечисление, которое подтягивает параметры с json файла
    """
    DEFAULT = QColor(settings["left_menu"]["color"])
    HOVER = QColor(settings["left_menu"]["color_hover"])
    PRESSED = QColor(settings["left_menu"]["color_pressed"])
