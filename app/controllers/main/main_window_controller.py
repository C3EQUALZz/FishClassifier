from app.core.abstract import AbstractController
from app.views.chat.page.page_messages import Chat
import logging

logger = logging.getLogger(__name__)


class MainController(AbstractController):
    def __init__(self, view):
        super().__init__(view)
        self.view = view
        logger.debug("MainController инициализирован")

        for neural_network in self.view.neural_networks:
            neural_network.clicked.connect(self.btn_clicked)
            neural_network.released.connect(self.btn_released)
            logger.debug(f"Добавил сигнал для {neural_network}")
        logger.debug("MainController сигналы подключены")

    def btn_clicked(self):
        logger.debug("Запущен btn_clicked")
        # GET BT CLICKED
        btn = self.view.sender()
        logger.debug(f'Нажата кнопка: {btn}')

        # UNSELECT CHATS
        self.view.ui.ui_functions.UiFunctions.deselect_other_chat_messages(self.view, btn.objectName())

        # SELECT CLICKED
        if btn.objectName():
            btn.reset_unread_message()
            self.view.ui.ui_functions.ui_functions.UiFunctions.select_chat_message(self.view, btn.objectName())

        # LOAD CHAT PAGE
        if btn.objectName():
            # REMOVE CHAT
            for chat in reversed(range(self.view.ui.chat_layout.count())):
                self.view.ui.chat_layout.itemAt(chat).widget().deleteLater()
            self.view.chat = None

            # SET CHAT WIDGET
            self.view.chat = Chat(btn.user_image, btn.user_name, btn.user_description, btn.objectName(),
                                  self.view.top_user.user_name)

            # ADD WIDGET TO LAYOUT
            self.view.ui.chat_layout.addWidget(self.view.chat)

            # JUMP TO CHAT PAGE
            self.view.ui.app_pages.setCurrentWidget(self.view.ui.chat)

        # DEBUG
        print(f"Button {btn.objectName()}, clicked!")

    def btn_released(self):
        # GET BT CLICKED
        btn = self.view.sender()
        print(F"Button {btn.objectName()}, released!")
