from PySide6.QtCore import Signal, Qt, QRect
from PySide6.QtGui import QPainter, QPainterPath, QPen, QBrush, QColor, QImage
from PySide6.QtWidgets import QGraphicsOpacityEffect

from PySide6.QtWidgets import QWidget, QFrame, QLabel
import os
import logging

logger = logging.getLogger(__name__)


class FriendMessageButton(QWidget):
    clicked = Signal()
    released = Signal()

    def __init__(self, _id, network_image, network_name, network_description, network_status, unread_messages,
                 is_active):
        super().__init__()

        self.user_image = os.path.join(os.path.abspath(os.getcwd()), network_image)
        self.user_name = network_name
        self.user_description = network_description
        self.user_status = network_status
        self.unread_messages = unread_messages
        self.is_active = is_active
        self._status_color = "#46b946"
        self.bg_color_entered = "#22CCCCCC"
        self.bg_color_leave = "#00000000"
        self.bg_color_active = "#33CCCCCC"
        self._bg_color = self.bg_color_leave

        self.setFixedSize(240, 50)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setObjectName(str(_id))
        self.setup_ui()

        if self.unread_messages > 0:
            self.label_messages.show()
            self.label_messages.setText(str(self.unread_messages))

        if self.user_status == "online":
            self._status_color = "#46b946"
        elif self.user_status == "idle":
            self._status_color = "#ff9955"
        elif self.user_status == "busy":
            self._status_color = "#a02c2c"
        elif self.user_status == "invisible":
            self._status_color = "#808080"
            self.opacity = QGraphicsOpacityEffect()
            self.opacity.setOpacity(0.4)
            self.setGraphicsEffect(self.opacity)

    def reset_unread_message(self):
        self.unread_messages = 0
        self.label_messages.hide()
        self.repaint()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.released.emit()

    def enterEvent(self, event):
        if not self.is_active:
            self._bg_color = self.bg_color_entered
            self.repaint()

    def leaveEvent(self, event):
        if not self.is_active:
            self._bg_color = self.bg_color_leave
            self.repaint()

    def set_active(self, active):
        self.is_active = active
        self._bg_color = self.bg_color_leave if not active else self.bg_color_active
        self.repaint()

    def setup_ui(self):
        self.text_frame = QFrame(self)
        self.text_frame.setGeometry(60, 0, 170, 50)

        self.label_user = QLabel(self.text_frame)
        self.label_user.setGeometry(0, 8, self.text_frame.width(), 20)
        self.label_user.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.label_user.setText(self.user_name.capitalize())
        self.label_user.setStyleSheet("color: #e7e7e7; font: 700 10pt 'Segoe UI';")

        self.label_description = QLabel(self.text_frame)
        self.label_description.setGeometry(0, 22, self.text_frame.width(), 18)
        self.label_description.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.label_description.setText(self.user_description)
        self.label_description.setStyleSheet("color: #A6A6A6; font: 9pt 'Segoe UI';")

        self.label_messages = QLabel(self)
        self.label_messages.setFixedSize(35, 20)
        self.label_messages.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_messages.setStyleSheet("""
            background-color: #1e2021;
            padding-left: 5px;
            padding-right: 5px;
            color: #bdff00;
            border-radius: 10px;
            border: 3px solid #333;
            font: 9pt 'Segoe UI';
        """)
        self.label_messages.move(self.width() - 45, 16)
        self.label_messages.hide()

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)

        rect = QRect(10, 5, 40, 40)

        painter.setBrush(QBrush(QColor(self._bg_color if not self.is_active else self.bg_color_active)))
        painter.drawRoundedRect(5, 0, 230, 50, 25, 25)

        painter.setBrush(QBrush(QColor("#000000")))
        painter.drawEllipse(rect)

        self.draw_user_image(painter, self.user_image, rect)

        painter.end()

        if self.user_status != "invisible":
            self.draw_status(self.user_image, rect)

    @staticmethod
    def draw_user_image(qp, image, rect):
        user_image = QImage(image)
        path = QPainterPath()
        path.addEllipse(rect)
        qp.setClipPath(path)
        qp.drawImage(rect, user_image)

    def draw_status(self, status, rect):
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        pen = QPen()
        pen.setWidth(3)
        pen.setColor(QColor("#151617"))
        painter.setPen(pen)

        painter.setBrush(QBrush(QColor(self._status_color)))

        painter.drawEllipse(rect.x() + 27, rect.y() + 27, 13, 13)
        painter.end()
