from PySide6.QtCore import QTimer, Qt

import logging
import app.core.abstract as abstract_namespace
import app.views.login as login_view_namespace

logger = logging.getLogger(__name__)


class LoginController(abstract_namespace.AbstractController):
    def __init__(self, view: login_view_namespace.LoginView) -> None:
        super().__init__(view)
        logger.debug("Инициализация LoginController")
        self.view.set_key_event_handlers(self.check_login)

    def check_login(self, event):
        def __open_main_window():
            # SHOW MAIN WINDOW
            self.window_manager.switch_to_window("MainWindowView")
            self.window_manager.get_current_window().top_user.label_user.setText(username.capitalize())

        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            username = self.view.ui.username.text()
            password = self.view.ui.password.text()

            if username and password == "123456":
                self.view.set_user_description(f"Welcome {username}!", "#user_description { color: #bdff00 }")
                self.view.set_username_style("#username:focus { border: 3px solid #bdff00; }")
                self.view.set_password_style("#password:focus { border: 3px solid #bdff00; }")
                QTimer.singleShot(1200, lambda: __open_main_window())
            else:
                self.view.set_username_style("#username:focus { border: 3px solid rgb(255, 0, 127); }")
                self.view.set_password_style("#password:focus { border: 3px solid rgb(255, 0, 127); }")
