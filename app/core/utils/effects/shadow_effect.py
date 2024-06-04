from PySide6.QtWidgets import QGraphicsDropShadowEffect
from PySide6.QtGui import QColor


class ShadowEffect(QGraphicsDropShadowEffect):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setBlurRadius(15)
        self.setXOffset(0)
        self.setYOffset(0)
        self.setColor(QColor(0, 0, 0, 160))
