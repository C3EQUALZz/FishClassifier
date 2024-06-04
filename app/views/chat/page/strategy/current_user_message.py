from PySide6.QtCore import Qt
import app.views.chat.page.helpers as page_helpers_namespace
from .interface import MessageStrategy


class UserMessageStrategy(MessageStrategy):
    """Стратегия отправки сообщений от пользователя."""

    def send_message(self, messages: str, parent) -> None:
        if parent.page.line_edit_message.text() != "":
            message = page_helpers_namespace.Message(parent.page.line_edit_message.text(), True, parent=parent)
            parent.page.chat_messages_layout.addWidget(message, Qt.AlignmentFlag.AlignCenter,
                                                       Qt.AlignmentFlag.AlignBottom)
            parent.page.line_edit_message.setText("")
