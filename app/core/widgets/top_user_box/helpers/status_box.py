from PySide6.QtGui import Qt
from PySide6.QtCore import Qt, QEvent
from PySide6.QtWidgets import QFrame, QWidget

import app.core.widgets.top_user_box.helpers as top_user_box_helpers_namespace
import logging


class StatusBox:
    """
    StatusBox представляет виджет, который отображает и изменяет статус пользователя.

    Attributes:
        parent (QWidget): Родительский виджет.
        status_color (str): Цвет текущего статуса.
        status_box (QFrame): Виджет, представляющий интерфейс изменения статуса.
    """

    def __init__(self, parent: QWidget):
        """
        Инициализация StatusBox.

        Args:
            parent (QWidget): Родительский виджет.
        """
        self.parent = parent
        self.status_color = None

        self.status_box = top_user_box_helpers_namespace.ChangeStatus(parent.parent_widget)
        self.status_box.focusOutEvent = self.lost_focus_status_box
        self.status_box.line_edit.focusOutEvent = self.lost_focus_line_edit
        self.status_box.line_edit.keyReleaseEvent = self.change_description
        self.status_box.hide()
        self.status_box.status.connect(self.change_status)

    def move(self, left: int, top: int) -> None:
        """
        Перемещает status_box на указанные координаты.

        Args:
            left (int): Координата X.
            top (int): Координата Y.
        """
        self.status_box.move(left, top)

    def lost_focus_status_box(self, event: QEvent) -> None:
        """
        Обрабатывает событие потери фокуса для status_box.

        Args:
            event (QEvent): Событие потери фокуса.
        """
        if not self.status_box.line_edit.hasFocus():
            self.status_box.hide()
            self.status_box.line_edit.setText("")

    def lost_focus_line_edit(self, event: QEvent) -> None:
        """
        Обрабатывает событие потери фокуса для line_edit.

        Args:
            event (QEvent): Событие потери фокуса.
        """
        if not self.status_box.hasFocus():
            self.status_box.hide()
            self.status_box.line_edit.setText("")

    def change_description(self, event: QEvent) -> None:
        """
        Обрабатывает изменение описания пользователя при нажатии Enter/Return.

        Args:
            event (QEvent): Событие нажатия клавиши.
        """
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            self.parent.label_description.setText(self.status_box.line_edit.text())
            self.status_box.line_edit.setText("")
            self.status_box.hide()

    def change_status(self, status: str) -> None:
        """
        Изменяет цвет статуса и обновляет интерфейс при получении нового статуса.

        Args:
            status (str): Новый статус пользователя.
        """
        match status:
            case "online":
                self.parent.status_color = "#46b946"
                logging.debug("Статус изменен на 'в сети'")
            case "idle":
                self.parent.status_color = "#ff9955"
                logging.debug("Статус изменен на 'неактивен'")
            case "busy":
                self.parent.status_color = "#a02c2c"
                logging.debug("Статус изменен на 'занят'")
            case "invisible":
                self.parent.status_color = "#808080"
                logging.debug("Статус изменен на 'невидимый'")
            case _:
                logging.warning(f"Неизвестный статус: {status}")
                return

        self.parent.repaint()
        self.parent.status.emit(status)
