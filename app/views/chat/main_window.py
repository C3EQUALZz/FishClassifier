import logging
import pathlib

from PySide6.QtWidgets import QMainWindow

import app.models.neural_network_model as models_neural_network
import app.modules.ui_functions.functions as ui_functions
from app.core.widgets import (
    LeftMenu,
    LeftMenuButton,
    TopUserInfo,
    FriendMessageButton,
)
from app.modules.app_settings.settings import Settings
from app.views.chat.helpers.ui_main import UiMainWindow

logger = logging.getLogger(__name__)


class MainView(QMainWindow):
    def __init__(self):
        super().__init__()
        logger.debug("Инициализация MainView")

        self.dragPos = None
        self.neural_networks = []

        self.ui = UiMainWindow()
        self.ui.setupUi(self)
        logger.debug("Настроился UiMainWindow")

        self.ui.app_pages.setCurrentWidget(self.ui.home)

        self.settings = Settings()
        logger.debug("Инициализация Settings")

        self.left_menu = LeftMenu()
        logger.debug("Инициализация LeftMenu")

        self.add_buttons_to_left_menu()
        logger.debug("Добавляет кнопки в левое меню")

        self.top_user = TopUserInfo(self.ui.left_messages, 8, 64, "", "Writing python codes")
        self.top_user.setParent(self.ui.top_user_frame)

        # SET UI DEFINITIONS
        # Run set_ui_definitions() in the ui_functions.py
        # ///////////////////////////////////////////////////////////////
        ui_functions.UiFunctions.set_ui_definitions(self)

        # ADD MESSAGE BTNS / FRIEND MENUS
        # Add btns to page
        # ///////////////////////////////////////////////////////////////

        self.add_menus(
            models_neural_network.NeuralNetworks(
                pathlib.Path(self.settings["neural_networks_path"])
            ).networks
        )

    def add_menus(self, users) -> None:
        for _id, user in enumerate(users):
            neural_network = FriendMessageButton(_id,
                                                 user_image=user.network_image,
                                                 user_name=user.network_name,
                                                 user_description=user.network_description,
                                                 user_status=user.network_status,
                                                 unread_messages=user.unread_messages,
                                                 is_active=user.is_active)

            self.neural_networks.append(neural_network)

            logger.debug(f"Кнопка добавлена: {neural_network.objectName()}")
            self.ui.messages_layout.addWidget(neural_network)

    def add_buttons_to_left_menu(self) -> None:
        button_config = self.settings['left_menu']['buttons']
        for button_name, button_info in button_config.items():
            button = LeftMenuButton(
                self,
                button_name,
                button_info["icon_path"],
                button_info["tooltip"]
            )
            self.left_menu[button_name] = button

            if button_name == 'add_new_friend':
                self.ui.top_menus_layout.addWidget(button)
            else:
                self.ui.bottom_menus_layout.addWidget(button)

    def show_window(self) -> None:
        """
        Метод для включения окна
        :return: ничего не возвращает, нужен для интерфейса
        """
        self.show()

    def hide_window(self) -> None:
        self.close()
