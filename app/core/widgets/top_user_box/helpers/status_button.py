from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPushButton


class StatusButton(QPushButton):
    def __init__(self, text, icon_path, parent=None):
        super().__init__(text, parent)
        self.setMinimumHeight(30)
        self.setStyleSheet(f"background-image: url({icon_path});")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
