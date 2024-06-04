import logging
import pathlib
import app.controllers.main as chat_namespace

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
from app.views.chat.page.page_messages import Chat

from neuron_interaction.custom_model import CustomModel
from neuron_interaction.mobileNetV2_model import MobileNetV2Model
from neuron_interaction.vgg16_model import VGG16Model
from neuron_interaction.custom_model_better import CustomModelBetter

logger = logging.getLogger(__name__)


class MainView(QMainWindow):
    def __init__(self):
        super().__init__()
        logger.debug("Инициализация MainView")
        self.settings = Settings()
        logger.debug("Инициализация Settings")

        self.dragPos = None
        self.neural_networks: list[FriendMessageButton] = []

        self.ui = UiMainWindow()
        self.ui.setupUi(self)
        logger.debug("Настроился UiMainWindow")

        self.ui_functions = ui_functions.UiFunctions

        self.add_chat_networks(
            models_neural_network.NeuralNetworks(
                pathlib.Path(self.settings["neural_networks_path"])
            ).networks
        )

        self.ui.app_pages.setCurrentWidget(self.ui.home)

        self.left_menu = LeftMenu()
        logger.debug("Инициализация LeftMenu")

        self.add_buttons_to_left_menu()
        logger.debug("Добавляет кнопки в левое меню")

        self.top_user = TopUserInfo(self.ui.left_messages, 8, 64, "", "Writing python codes")
        self.top_user.setParent(self.ui.top_user_frame)

        self.ui_functions.set_ui_definitions(self)

    def add_chat_networks(self, networks: list[models_neural_network.NeuralNetwork]) -> None:
        for _id, network in enumerate(networks):
            neural_network = FriendMessageButton(_id, network)

            self.neural_networks.append(neural_network)
            neural_network.clicked.connect(self.btn_clicked)
            neural_network.released.connect(self.btn_released)

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

    def btn_clicked(self):
        logger.debug("Запущен btn_clicked")
        last_pressed_button: FriendMessageButton = self.sender()
        logger.debug(f'Нажата кнопка: {last_pressed_button}')

        # UNSELECT CHATS
        self.ui_functions.deselect_other_chat_messages(self, last_pressed_button.objectName())

        # SELECT CLICKED
        if last_pressed_button.objectName():
            last_pressed_button.reset_unread_message()
            self.ui_functions.select_chat_message(self, last_pressed_button.objectName())

        # LOAD CHAT PAGE
        if last_pressed_button.objectName():
            # REMOVE CHAT
            for chat in reversed(range(self.ui.chat_layout.count())):
                self.ui.chat_layout.itemAt(chat).widget().deleteLater()

            view = Chat(my_name=self.top_user.user_name,
                        image_path=last_pressed_button.user_image)

            model = None

            if last_pressed_button.objectName() == "0":
                model = CustomModel()

            if last_pressed_button.objectName() == "1":
                model = VGG16Model()

            if last_pressed_button.objectName() == "2":
                model = MobileNetV2Model()

            if last_pressed_button.objectName() == "3":
                model = CustomModelBetter()

            self.chat = chat_namespace.ChatController(view=view,
                                                      model=model,
                                                      network=last_pressed_button.network,
                                                      my_name=self.top_user.user_name)

            # ADD WIDGET TO LAYOUT
            self.ui.chat_layout.addWidget(view)

            # JUMP TO CHAT PAGE
            self.ui.app_pages.setCurrentWidget(self.ui.chat)

        # DEBUG
        print(f"Button {last_pressed_button.objectName()}, clicked!")

    def btn_released(self):
        # GET BT CLICKED
        btn = self.sender()
        print(F"Button {btn.objectName()}, released!")
