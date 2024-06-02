from PySide6.QtGui import *
from PySide6.QtWidgets import *


class ToolTip(QLabel):
    def __init__(self, parent, tooltip: str, style_tooltip: str):
        super().__init__()

        self.opacity = QGraphicsOpacityEffect(self)
        self.shadow = QGraphicsDropShadowEffect(self)
        self.setup_label(parent, tooltip, style_tooltip)

    def setup_label(self, parent: QWidget, tooltip_text: str, style_tooltip: str) -> None:
        """
        Устанавливает параметры метки с заданными параметрами.
        """
        self.setObjectName(u"label_tooltip")
        self.setStyleSheet(style_tooltip)
        self.setMinimumHeight(36)
        self.setParent(parent)
        self.setText(tooltip_text)
        self.adjustSize()

    @property
    def shadow(self):
        """
        Возвращает эффект тени.
        """
        return self._shadow

    @shadow.setter
    def shadow(self, shadow_ef: QGraphicsDropShadowEffect) -> None:
        """
        Устанавливает эффект тени.
        """
        shadow_ef.setBlurRadius(15)
        shadow_ef.setXOffset(0)
        shadow_ef.setYOffset(0)
        shadow_ef.setColor(QColor(0, 0, 0, 160))
        self.setGraphicsEffect(shadow_ef)
        self._shadow = shadow_ef

    @property
    def opacity(self):
        """
        Возвращает эффект прозрачности.
        """
        return self._opacity

    @opacity.setter
    def opacity(self, opacity_ef: QGraphicsOpacityEffect) -> None:
        """
        Устанавливает эффект прозрачности.
        """
        opacity_ef.setOpacity(0.85)
        self.setGraphicsEffect(opacity_ef)
        self._opacity = opacity_ef
