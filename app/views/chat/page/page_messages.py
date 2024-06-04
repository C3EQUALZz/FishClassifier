from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
import app.views.chat.page.helpers as page_helpers_namespace
import os


class Chat(QWidget):
    message_sent = Signal(str)
    image_sent = Signal(str)

    def __init__(self, my_name, image_path, parent=None):
        super().__init__(parent)
        self.page = page_helpers_namespace.Ui_chat_page()
        self.page.setupUi(self)

        self.page.user_image.setStyleSheet("#user_image { background-image: url(\"" +
                                           os.path.normpath(image_path).replace("\\", "/") + "\") }")

        self.page.line_edit_message.keyReleaseEvent = self.on_enter_return_release
        self.page.btn_send_message.clicked.connect(self.on_send_message_clicked)
        self.page.btn_emoticon.clicked.connect(
            self.on_send_image_clicked)  # Assuming there is a button for sending images

    def update_user_info(self, network_name, network_description):
        self.page.user_name.setText(network_name)
        self.page.user_description.setText(network_description)
        format_user_name = network_name.replace(" ", "_").replace("-", "_").lower()
        self.page.line_edit_message.setPlaceholderText(f"Message #{format_user_name}")

    def on_enter_return_release(self, event):
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            self.on_send_message_clicked()

    def on_send_message_clicked(self):
        text = self.page.line_edit_message.text()
        self.page.line_edit_message.clear()
        self.message_sent.emit(text)

    def on_send_image_clicked(self):
        image_path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Image Files (*.png *.jpg *.jpeg)")
        if image_path:
            self.image_sent.emit(image_path)

    def display_message(self, message, sender):
        if sender == "user":
            self.add_user_message(message)
        elif sender == "friend":
            self.add_friend_message(message)
        self.scroll_to_end()

    def add_user_message(self, message):
        user_message_label = QLabel(message)
        user_message_label.setStyleSheet("background-color: lightblue; border-radius: 5px; padding: 5px;")
        self.page.chat_messages_layout.addWidget(user_message_label)

    def add_friend_message(self, message):
        friend_message_label = QLabel(message)
        friend_message_label.setStyleSheet("background-color: lightgreen; border-radius: 5px; padding: 5px;")
        self.page.chat_messages_layout.addWidget(friend_message_label)

    def add_image_message(self, image_path, sender):
        image_label = QLabel()
        pixmap = QPixmap(image_path)
        image_label.setPixmap(pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio))  # Adjust the size as needed
        if sender == "user":
            image_label.setStyleSheet("background-color: lightblue; border-radius: 5px; padding: 5px;")
        elif sender == "friend":
            image_label.setStyleSheet("background-color: lightgreen; border-radius: 5px; padding: 5px;")
        self.page.chat_messages_layout.addWidget(image_label)

    def scroll_to_end(self):
        self.scroll_bar = self.page.chat_messages.verticalScrollBar()
        self.scroll_bar.setValue(self.scroll_bar.maximum())
