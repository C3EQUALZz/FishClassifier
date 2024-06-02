from PySide6.QtCore import *
from PySide6.QtGui import QColor
from PySide6.QtWidgets import *

import app.core as core
import app.core.base.decorators as decorators_namespace
import app.views.login.helpers as helpers_namespace


class LoginView(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = helpers_namespace.UiLogin()
        self.ui.setupUi(self)

        self.progress_bar = decorators_namespace.MenuProgress(core.CircularProgress(), self.ui)
        self.shadow = QGraphicsDropShadowEffect(self)

        self.init_ui()

    def init_ui(self):
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.progress_bar.start()

        self.shadow.setBlurRadius(15)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 80))
        self.ui.bg.setGraphicsEffect(self.shadow)

        self.show()

    def set_username_style(self, style):
        self.ui.username.setStyleSheet(style)

    def set_password_style(self, style):
        self.ui.password.setStyleSheet(style)

    def set_user_description(self, text, style):
        self.ui.user_description.setText(text)
        self.ui.user_description.setStyleSheet(style)

    def set_key_event_handlers(self, handler):
        self.ui.username.keyReleaseEvent = handler
        self.ui.password.keyReleaseEvent = handler

    def move_window(self, x, y):
        self.move(x, y)

    def shackle_window(self):
        actual_position = self.pos()
        offsets = (1, -2, 4, -5, 4, -2, 0)
        for i, offset in enumerate(offsets):
            QTimer.singleShot(i * 50, lambda: self.move(actual_position.x() + offset, actual_position.y()))

    def show_window(self):
        self.show()

    def hide_window(self):
        self.close()
