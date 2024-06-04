from app.core.abstract import AbstractController
from app.views.chat.page.page_messages import Chat
from PySide6 import QtCore
import logging
from abc import ABCMeta
import app.views.chat.main_window as main_window_namespace

logger = logging.getLogger(__name__)


class MainControllerMeta(type(QtCore.QObject), ABCMeta):
    pass


class MainController(AbstractController, QtCore.QObject, metaclass=MainControllerMeta):
    def __init__(self, view: main_window_namespace.MainView):
        super().__init__(view)
        self.view = view
        logger.debug(f"MainController принял view: {view}")

    def initialize(self):
        ...
        # for neural_network in self.view.neural_networks:
        #     neural_network.clicked.connect(self.btn_clicked)
        #     neural_network.released.connect(self.btn_released)
        #     logger.debug(f"Добавил сигнал для {neural_network}")
        # logger.debug("MainController сигналы подключены")

    @QtCore.Slot()
    def btn_clicked(self):
        logger.debug("Запущен btn_clicked")
        # GET BT CLICKED
        btn = self.view.sender()
        logger.debug(f'Нажата кнопка: {btn}')

        # UNSELECT CHATS
        self.view.ui_functions.deselect_other_chat_messages(self, btn.objectName())

        # SELECT CLICKED
        if btn.objectName():
            btn.reset_unread_message()
            self.view.ui_functions.select_chat_message(self, btn.objectName())

        # LOAD CHAT PAGE
        if btn.objectName():
            # REMOVE CHAT
            for chat in reversed(range(self.view.ui.chat_layout.count())):
                self.view.ui.chat_layout.itemAt(chat).widget().deleteLater()
            self.chat = None

            # SET CHAT WIDGET
            self.chat = Chat(btn.user_image, btn.user_name, btn.user_description, btn.objectName(),
                             self.view.top_user.user_name, parent=self.view)

            # ADD WIDGET TO LAYOUT
            self.view.ui.chat_layout.addWidget(self.chat)

            # JUMP TO CHAT PAGE
            self.view.ui.app_pages.setCurrentWidget(self.view.ui.chat)

        # DEBUG
        print(f"Button {btn.objectName()}, clicked!")

    @QtCore.Slot()
    def btn_released(self):
        # GET BT CLICKED
        btn = self.view.sender()
        print(F"Button {btn.objectName()}, released!")
