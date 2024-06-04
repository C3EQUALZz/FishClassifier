# ///////////////////////////////////////////////////////////////
#
# BY: WANDERSON M.PIMENTA
# PROJECT MADE WITH: Qt Designer and PySide6
# V: 1.0.0
#
# This project can be used freely for all uses, as long as they maintain the
# respective credits only in the Python scripts, any information in the visual
# interface (GUI) can be modified without any implication.
#
# There are limitations on Qt licenses if you want to use your products
# commercially, I recommend reading them on the official website:
# https://doc.qt.io/qtforpython/licenses.html
#
# ///////////////////////////////////////////////////////////////

# DEFAULT PACKAGES
# ///////////////////////////////////////////////////////////////
import os

# IMPORT / GUI, SETTINGS AND WIDGETS
# ///////////////////////////////////////////////////////////////
# Packages
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

import app.views.chat.page.strategy as message_strategy_namespace

# GUI
import app.views.chat.page.helpers as page_helpers_namespace


# MAIN WINDOW
# ///////////////////////////////////////////////////////////////
class Chat(QWidget):
    def __init__(self, user_image, user_name, user_description, user_id, my_name, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.page = page_helpers_namespace.Ui_chat_page()
        self.page.setupUi(self)

        # UPDATE INFO
        self.page.user_image.setStyleSheet("#user_image { background-image: url(\"" +
                                           os.path.normpath(user_image).replace("\\", "/") + "\") }"
                                           )

        self.page.user_name.setText(user_name)
        self.page.user_description.setText(user_description)

        # CHANGE PLACEHOLDER TEXT
        format_user_name = user_name.replace(" ", "_").replace("-", "_")
        format_user_name = format_user_name.lower()
        self.page.line_edit_message.setPlaceholderText(f"Message #{str(format_user_name).lower()}")

        # ENTER / RETURN PRESSED
        self.page.line_edit_message.keyReleaseEvent = self.enter_return_release

        # ENTER / RETURN PRESSED
        self.page.btn_send_message.clicked.connect(self.send_message)

        # MESSAGES
        self.messages = [
            f"Hi {my_name.capitalize()}, how are you?",
            f"Hello {my_name.capitalize()}, how are you today?",
            f"{my_name.capitalize()}, do you know if it is going to rain today?",
            f"{my_name.capitalize()}, how is your day?",
            f"{my_name.capitalize()}, do you remember that you owe me $100? Humm..."
        ]

        self.friend_message_strategy = message_strategy_namespace.FriendMessageStrategy()
        self.user_message_strategy = message_strategy_namespace.UserMessageStrategy()

    # ENTER / RETURN SEND MESSAGE
    def enter_return_release(self, event):
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            self.send_message()

    # SEND MESSAGE
    def send_message(self):
        self.user_message_strategy.send_message(self.messages[0], self)

        # SCROLL TO END
        QTimer.singleShot(10, lambda: self.page.messages_frame.setFixedHeight(
            self.page.chat_messages_layout.sizeHint().height()))
        QTimer.singleShot(15, lambda: self.scroll_to_end())

        # SEND USER MESSAGE
        QTimer.singleShot(1000, lambda: self.send_by_friend())

    # SEND MESSAGE BY FRIEND
    def send_by_friend(self):
        self.friend_message_strategy.send_message(self.messages[0], self)

        # SCROLL TO END
        QTimer.singleShot(10, lambda: self.page.messages_frame.setFixedHeight(
            self.page.chat_messages_layout.sizeHint().height()))
        QTimer.singleShot(15, lambda: self.scroll_to_end())

    def scroll_to_end(self):
        # SCROLL TO END
        self.scroll_bar = self.page.chat_messages.verticalScrollBar()
        self.scroll_bar.setValue(self.scroll_bar.maximum())
