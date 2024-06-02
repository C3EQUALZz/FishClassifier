import logging

from PySide6.QtWidgets import *

import app.modules.ui_functions.functions as ui_functions
from app.core.widgets import *
from app.modules.app_settings.settings import *
from app.views.chat.helpers.ui_main import UiMainWindow

logger = logging.getLogger(__name__)


class MainView(QMainWindow):
    def __init__(self):
        super().__init__()
        logger.debug("Инициализация MainView")

        self.dragPos = None
        self.ui = UiMainWindow()
        self.ui.setupUi(self)
        logger.debug("Настроился UiMainWindow")

        # SET DEFAULT PAGE
        # ///////////////////////////////////////////////////////////////
        self.ui.app_pages.setCurrentWidget(self.ui.home)

        # LOAD DICT SETTINGS FROM "settings.json" FILE
        # ///////////////////////////////////////////////////////////////
        self.settings = Settings()
        logger.debug("Инициализация Settings")

        self.left_menu = LeftMenu()
        logger.debug("Инициализация LeftMenu")

        self.add_buttons_to_left_menu()
        logger.debug("Добавляет кнопки в левое меню")

        # TOP USER BOX
        # Add widget to App
        # ///////////////////////////////////////////////////////////////
        self.top_user = TopUserInfo(self.ui.left_messages, 8, 64, "wanderson", "Writing python codes")
        self.top_user.setParent(self.ui.top_user_frame)

        # SET UI DEFINITIONS
        # Run set_ui_definitions() in the ui_functions.py
        # ///////////////////////////////////////////////////////////////
        ui_functions.UiFunctions.set_ui_definitions(self)

        # ADD MESSAGE BTNS / FRIEND MENUS
        # Add btns to page
        # ///////////////////////////////////////////////////////////////
        add_user = [
            {
                "user_image": "images/users/cat.png",
                "user_name": "Tom",
                "user_description": "Did you see a mouse?",
                "user_status": "online",
                "unread_messages": 2,
                "is_active": False
            },
            {
                "user_image": "images/users/mouse.png",
                "user_name": "Jerry",
                "user_description": "I think I saw a cat...",
                "user_status": "busy",
                "unread_messages": 1,
                "is_active": False
            },

        ]
        self.menu = FriendMessageButton

        self.add_menus(add_user)

    def add_menus(self, parameters):
        _id = 0
        for parameter in parameters:
            user_image = parameter['user_image']
            user_name = parameter['user_name']
            user_description = parameter['user_description']
            user_status = parameter['user_status']
            unread_messages = parameter['unread_messages']
            is_active = parameter['is_active']

            self.menu = FriendMessageButton(
                _id, user_image, user_name, user_description, user_status, unread_messages, is_active
            )
            self.ui.messages_layout.addWidget(self.menu)
            _id += 1

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
