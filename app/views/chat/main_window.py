import logging
import pathlib
import dataclasses

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
        self.menu = None

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

        self.add_menus(models_neural_network.NeuralNetworks(pathlib.Path('app/resources/users.json')).networks)

    def add_menus(self, users) -> None:
        for _id, user in enumerate(users):
            self.menu = FriendMessageButton(_id, **dataclasses.asdict(user))
            self.ui.messages_layout.addWidget(self.menu)

    def add_buttons_to_left_menu(self) -> None:
        self.left_menu['custom_btn_top'] = LeftMenuButton(
            self,
            "custom_btn_top",
            "app/resources/images/icons_svg/icon_add_user.svg",
            "Add new friend"
        )

        self.left_menu['custom_btn_bottom_1'] = LeftMenuButton(
            self,
            "custom_btn_bottom_1",
            "app/resources/images/icons_svg/icon_more_options.svg",
            "More options, test with many words"
        )

        self.left_menu['custom_btn_bottom_2'] = LeftMenuButton(
            self,
            "custom_btn_bottom_2",
            "app/resources/images/icons_svg/icon_settings.svg",
            "Open settings"
        )

        # Add buttons to layouts
        self.ui.top_menus_layout.addWidget(self.left_menu['custom_btn_top'])
        self.ui.bottom_menus_layout.addWidget(self.left_menu['custom_btn_bottom_1'])
        self.ui.bottom_menus_layout.addWidget(self.left_menu['custom_btn_bottom_2'])

    def show_window(self) -> None:
        """
        Метод для включения окна
        :return: ничего не возвращает, нужен для интерфейса
        """
        self.show()

    def hide_window(self) -> None:
        self.close()
