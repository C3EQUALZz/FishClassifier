from PySide6.QtCore import Qt
import app.views.chat.page.helpers as page_helpers_namespace
from .interface import MessageStrategy


class FriendMessageStrategy(MessageStrategy):
    """Стратегия отправки сообщений от друга."""

    def send_message(self, message: str, parent) -> None:
        message = page_helpers_namespace.Message(message, False, parent=parent)
        parent.page.chat_messages_layout.addWidget(message, Qt.AlignmentFlag.AlignCenter, Qt.AlignmentFlag.AlignBottom)
        parent.page.line_edit_message.setText("")
